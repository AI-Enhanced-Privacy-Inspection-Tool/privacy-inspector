"""
Active Website Detection Module

This module detects currently active websites from browser processes and history.
It can identify which websites are currently open in browser tabs and recent browsing history.
"""

import os
import re
import sqlite3
import json
from typing import List, Dict, Set, Optional
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ActiveWebsiteDetector:
    """
    Detects active and recent websites from browser data and processes.
    
    Supports:
    - Chrome/Chromium (history, cookies, cache)
    - Firefox (history, cookies)
    - Edge (Chromium-based, similar to Chrome)
    - Safari (macOS)
    """
    
    def __init__(self):
        """Initialize the website detector."""
        self.home_dir = Path.home()
        self.detected_websites: Set[str] = set()
    
    def get_active_websites(self, browser: Optional[str] = None) -> List[Dict]:
        """
        Get currently active or recently visited websites.
        
        Args:
            browser (str): Specific browser to scan ('chrome', 'firefox', 'edge', 'all')
            If None, scans all available browsers
            
        Returns:
            List[Dict]: List of websites with metadata
        """
        websites = []
        
        if browser is None or browser.lower() == 'all':
            websites.extend(self._get_chrome_websites())
            websites.extend(self._get_firefox_websites())
            websites.extend(self._get_edge_websites())
        elif browser.lower() == 'chrome':
            websites.extend(self._get_chrome_websites())
        elif browser.lower() == 'firefox':
            websites.extend(self._get_firefox_websites())
        elif browser.lower() == 'edge':
            websites.extend(self._get_edge_websites())
        
        # Remove duplicates based on domain
        unique_websites = []
        seen_domains = set()
        for site in sorted(websites, key=lambda x: x.get('last_visit', ''), reverse=True):
            domain = self._extract_domain(site['url'])
            if domain not in seen_domains:
                unique_websites.append(site)
                seen_domains.add(domain)
        
        return unique_websites
    
    def _get_chrome_websites(self) -> List[Dict]:
        """
        Extract websites from Chrome history and database.
        
        Returns:
            List[Dict]: List of visited websites
        """
        websites = []
        chrome_paths = [
            self.home_dir / 'AppData' / 'Local' / 'Google' / 'Chrome' / 'User Data' / 'Default',
            self.home_dir / 'AppData' / 'Local' / 'Chromium' / 'User Data' / 'Default',
        ]
        
        for chrome_path in chrome_paths:
            if not chrome_path.exists():
                continue
            
            try:
                # Chrome keeps history in a database
                history_db = chrome_path / 'History'
                if history_db.exists():
                    websites.extend(self._read_chrome_history(history_db))
                
                # Check cookies for session info
                cookies_db = chrome_path / 'Cookies'
                if cookies_db.exists():
                    websites.extend(self._read_chrome_cookies(cookies_db))
                    
            except Exception as e:
                logger.warning(f"Error reading Chrome data: {e}")
        
        return websites
    
    def _read_chrome_history(self, history_db_path: Path) -> List[Dict]:
        """
        Read Chrome history database.
        
        Args:
            history_db_path (Path): Path to Chrome History database
            
        Returns:
            List[Dict]: List of websites from history
        """
        websites = []
        
        try:
            # Chrome databases are locked when browser is open, so we need to handle this
            conn = sqlite3.connect(f'file:{history_db_path}?mode=ro', uri=True, timeout=2)
            cursor = conn.cursor()
            
            # Get recent history (last 7 days)
            seven_days_ago = (datetime.now() - timedelta(days=7)).timestamp() * 1_000_000
            
            cursor.execute("""
                SELECT DISTINCT url, title, last_visit_time
                FROM urls
                WHERE last_visit_time > ?
                ORDER BY last_visit_time DESC
                LIMIT 100
            """, (seven_days_ago,))
            
            for row in cursor.fetchall():
                url, title, timestamp = row
                if url and url.startswith(('http://', 'https://')):
                    websites.append({
                        'url': url,
                        'title': title or 'Unknown',
                        'last_visit': datetime.fromtimestamp(timestamp / 1_000_000).isoformat(),
                        'source': 'chrome_history',
                        'browser': 'Chrome'
                    })
            
            conn.close()
        except (sqlite3.OperationalError, sqlite3.DatabaseError):
            logger.debug("Chrome database is locked (browser may be running)")
        
        return websites
    
    def _read_chrome_cookies(self, cookies_db_path: Path) -> List[Dict]:
        """
        Read Chrome cookies to identify domains.
        
        Args:
            cookies_db_path (Path): Path to Chrome Cookies database
            
        Returns:
            List[Dict]: List of websites from cookies
        """
        websites = []
        
        try:
            conn = sqlite3.connect(f'file:{cookies_db_path}?mode=ro', uri=True, timeout=2)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT host_key, creation_utc
                FROM cookies
                ORDER BY creation_utc DESC
                LIMIT 50
            """)
            
            for row in cursor.fetchall():
                host, timestamp = row
                if host:
                    # Convert host_key to URL
                    if host.startswith('.'):
                        host = host[1:]
                    
                    websites.append({
                        'url': f'https://{host}',
                        'title': host,
                        'last_visit': datetime.fromtimestamp(timestamp / 1_000_000).isoformat(),
                        'source': 'chrome_cookies',
                        'browser': 'Chrome'
                    })
            
            conn.close()
        except (sqlite3.OperationalError, sqlite3.DatabaseError):
            logger.debug("Chrome Cookies database is locked")
        
        return websites
    
    def _get_firefox_websites(self) -> List[Dict]:
        """
        Extract websites from Firefox history.
        
        Returns:
            List[Dict]: List of visited websites
        """
        websites = []
        firefox_path = self.home_dir / 'AppData' / 'Roaming' / 'Mozilla' / 'Firefox' / 'Profiles'
        
        if not firefox_path.exists():
            return websites
        
        try:
            # Find the default profile
            for profile_dir in firefox_path.iterdir():
                if profile_dir.is_dir():
                    history_db = profile_dir / 'places.sqlite'
                    if history_db.exists():
                        websites.extend(self._read_firefox_history(history_db))
                        break  # Only read first profile
        except Exception as e:
            logger.warning(f"Error reading Firefox data: {e}")
        
        return websites
    
    def _read_firefox_history(self, history_db_path: Path) -> List[Dict]:
        """
        Read Firefox history database.
        
        Args:
            history_db_path (Path): Path to Firefox places.sqlite
            
        Returns:
            List[Dict]: List of websites from history
        """
        websites = []
        
        try:
            conn = sqlite3.connect(f'file:{history_db_path}?mode=ro', uri=True, timeout=2)
            cursor = conn.cursor()
            
            # Get recent history
            cursor.execute("""
                SELECT DISTINCT h.url, h.title, h.last_visit_date
                FROM moz_historyvisits v
                JOIN moz_places h ON v.place_id = h.id
                WHERE h.url LIKE 'http%'
                ORDER BY v.visit_date DESC
                LIMIT 100
            """)
            
            for row in cursor.fetchall():
                url, title, timestamp = row
                if url:
                    # Firefox timestamp is in microseconds
                    visit_time = datetime.fromtimestamp(timestamp / 1_000_000) if timestamp else datetime.now()
                    websites.append({
                        'url': url,
                        'title': title or 'Unknown',
                        'last_visit': visit_time.isoformat(),
                        'source': 'firefox_history',
                        'browser': 'Firefox'
                    })
            
            conn.close()
        except (sqlite3.OperationalError, sqlite3.DatabaseError):
            logger.debug("Firefox database is locked")
        
        return websites
    
    def _get_edge_websites(self) -> List[Dict]:
        """
        Extract websites from Microsoft Edge history.
        
        Returns:
            List[Dict]: List of visited websites
        """
        websites = []
        edge_path = self.home_dir / 'AppData' / 'Local' / 'Microsoft' / 'Edge' / 'User Data' / 'Default'
        
        if not edge_path.exists():
            return websites
        
        try:
            history_db = edge_path / 'History'
            if history_db.exists():
                websites.extend(self._read_chrome_history(history_db))
                
                # Update browser info
                for website in websites:
                    website['browser'] = 'Edge'
                    if 'chrome_' in website.get('source', ''):
                        website['source'] = website['source'].replace('chrome_', 'edge_')
        except Exception as e:
            logger.warning(f"Error reading Edge data: {e}")
        
        return websites
    
    def _extract_domain(self, url: str) -> str:
        """
        Extract domain from URL.
        
        Args:
            url (str): Full URL
            
        Returns:
            str: Domain name
        """
        try:
            # Remove protocol
            domain = url.replace('https://', '').replace('http://', '')
            # Remove path
            domain = domain.split('/')[0]
            # Remove port
            domain = domain.split(':')[0]
            return domain.lower()
        except:
            return url
    
    def get_suspicious_websites(self, websites: List[Dict]) -> List[Dict]:
        """
        Identify potentially suspicious websites from the list.
        
        Args:
            websites (List[Dict]): List of websites to analyze
            
        Returns:
            List[Dict]: List of suspicious websites with reasons
        """
        suspicious = []
        
        # Known suspicious patterns
        suspicious_patterns = [
            r'.*malware.*',
            r'.*phishing.*',
            r'.*adult.*',
            r'.*torrent.*',
            r'.*crack.*',
            r'.*keygen.*',
            r'.*porn.*',
        ]
        
        for website in websites:
            url = website['url'].lower()
            domain = self._extract_domain(url)
            
            reasons = []
            
            for pattern in suspicious_patterns:
                if re.match(pattern, domain):
                    reasons.append(f'Suspicious domain pattern detected: {pattern}')
            
            if reasons:
                suspicious.append({
                    'url': website['url'],
                    'domain': domain,
                    'browser': website.get('browser'),
                    'last_visit': website.get('last_visit'),
                    'reasons': reasons,
                    'risk_level': 'high'
                })
        
        return suspicious

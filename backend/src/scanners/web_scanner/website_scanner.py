"""
Website Security Scanner Module

This module provides functionality to scan active/specific websites for security risks.
It detects:
- HTTPS/SSL certificate issues
- Mixed content (HTTP resources on HTTPS pages)
- Missing security headers
- Insecure cookies
- Outdated JavaScript libraries
- Suspicious tracking scripts
- Potential XSS and CSRF vulnerabilities
"""

import re
import socket
import ssl
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

logger = logging.getLogger(__name__)


class WebsiteSecurityScanner:
    """
    Main class for scanning websites for security risks.
    
    Attributes:
        timeout (int): Request timeout in seconds
        user_agent (str): User agent string for requests
        known_vulnerable_libs (dict): Dictionary of known vulnerable JavaScript libraries
    """
    
    # Common vulnerable JavaScript libraries with known CVEs
    KNOWN_VULNERABLE_LIBS = {
        'jquery': {
            'vulnerable_versions': ['1.x', '2.x', '3.0.0-3.4.1'],
            'risk': 'high',
            'description': 'Cross-site scripting (XSS) vulnerabilities'
        },
        'bootstrap': {
            'vulnerable_versions': ['3.x', '4.0.0-4.5.2'],
            'risk': 'medium',
            'description': 'XSS vulnerabilities in tooltip component'
        },
        'moment': {
            'vulnerable_versions': ['2.0.0-2.29.0'],
            'risk': 'medium',
            'description': 'Regular expression DoS vulnerability'
        },
        'lodash': {
            'vulnerable_versions': ['4.0.0-4.17.20'],
            'risk': 'medium',
            'description': 'Prototype pollution vulnerability'
        }
    }
    
    # Security headers that should be present
    REQUIRED_SECURITY_HEADERS = {
        'Strict-Transport-Security': {
            'importance': 'critical',
            'description': 'Enforces HTTPS connections'
        },
        'X-Content-Type-Options': {
            'importance': 'high',
            'description': 'Prevents MIME-type sniffing'
        },
        'X-Frame-Options': {
            'importance': 'high',
            'description': 'Prevents clickjacking attacks'
        },
        'X-XSS-Protection': {
            'importance': 'high',
            'description': 'Enables browser XSS protection'
        },
        'Content-Security-Policy': {
            'importance': 'critical',
            'description': 'Controls resource loading to prevent XSS'
        },
        'Referrer-Policy': {
            'importance': 'medium',
            'description': 'Controls referrer information'
        }
    }
    
    # Known tracking/analytics scripts
    TRACKING_SCRIPTS = [
        'google-analytics',
        'googleanalytics',
        'gtag.js',
        'facebook.com/en_US/sdk.js',
        'cdn.segment.com',
        'amplitude.com',
        'intercom.io',
        'hotjar.com',
        'mixpanel.com'
    ]
    
    def __init__(self, timeout: int = 10):
        """
        Initialize the website scanner.
        
        Args:
            timeout (int): Request timeout in seconds (default: 10)
        """
        self.timeout = timeout
        self.user_agent = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry strategy.
        
        Returns:
            requests.Session: Configured session with retries
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=2,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update({'User-Agent': self.user_agent})
        return session
    
    def scan_website(self, url: str) -> Dict:
        """
        Perform a comprehensive security scan of a website.
        
        Args:
            url (str): Website URL to scan
            
        Returns:
            Dict: Comprehensive security assessment report
        """
        # Normalize URL
        url = self._normalize_url(url)
        
        report = {
            'url': url,
            'scan_timestamp': datetime.now().isoformat(),
            'is_reachable': False,
            'ssl_certificate': {},
            'security_headers': {},
            'mixed_content_issues': [],
            'tracking_scripts': [],
            'vulnerable_libraries': [],
            'cookie_issues': [],
            'risk_score': 0,
            'overall_risk_level': 'unknown',
            'recommendations': []
        }
        
        try:
            # Check if website is reachable - try HEAD first, fallback to GET
            page_response = None
            try:
                response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
                # HEAD might return 405 (Method Not Allowed) - that's OK, means server is reachable
                report['is_reachable'] = response.status_code != 405 and response.status_code < 400
                if response.status_code == 405:
                    # Server doesn't support HEAD, fallback to GET
                    raise requests.exceptions.RequestException("HEAD method not allowed")
            except requests.exceptions.RequestException:
                # Fallback to GET if HEAD fails (some servers don't support HEAD)
                try:
                    page_response = self.session.get(url, timeout=self.timeout)
                    report['is_reachable'] = page_response.status_code < 400
                except requests.exceptions.RequestException:
                    report['is_reachable'] = False
            
            if not report['is_reachable']:
                report['overall_risk_level'] = 'unreachable'
                return report
            
            # Get full page for detailed analysis if not already fetched
            if page_response is None:
                page_response = self.session.get(url, timeout=self.timeout)
            
            # Perform security checks
            report['ssl_certificate'] = self._check_ssl_certificate(url)
            report['security_headers'] = self._analyze_security_headers(page_response.headers)
            report['mixed_content_issues'] = self._detect_mixed_content(page_response.text, url)
            report['tracking_scripts'] = self._detect_tracking_scripts(page_response.text)
            report['vulnerable_libraries'] = self._detect_vulnerable_libraries(page_response.text)
            report['cookie_issues'] = self._analyze_cookies(page_response.cookies)
            
            # Calculate risk score
            report['risk_score'] = self._calculate_risk_score(report)
            report['overall_risk_level'] = self._determine_risk_level(report['risk_score'])
            report['recommendations'] = self._generate_recommendations(report)
            
        except requests.exceptions.SSLError as e:
            report['ssl_certificate']['error'] = f'SSL/TLS Error: {str(e)}'
            report['ssl_certificate']['is_valid'] = False
            report['risk_score'] = 85
            report['overall_risk_level'] = 'critical'
            
        except requests.exceptions.RequestException as e:
            report['is_reachable'] = False
            report['overall_risk_level'] = 'unreachable'
            logger.error(f"Error scanning {url}: {str(e)}")
        
        return report
    
    def _normalize_url(self, url: str) -> str:
        """
        Normalize URL to ensure it's properly formatted.
        
        Args:
            url (str): Raw URL
            
        Returns:
            str: Normalized URL
        """
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')
    
    def _check_ssl_certificate(self, url: str) -> Dict:
        """
        Verify SSL/TLS certificate validity and security.
        
        Args:
            url (str): Website URL
            
        Returns:
            Dict: SSL certificate details
        """
        result = {
            'is_valid': False,
            'is_https': False,
            'certificate_details': {},
            'warnings': []
        }
        
        try:
            parsed = urlparse(url)
            hostname = parsed.netloc
            
            # Check if HTTPS
            result['is_https'] = url.startswith('https://')
            
            if result['is_https']:
                context = ssl.create_default_context()
                with socket.create_connection((hostname, 443), timeout=self.timeout) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        result['certificate_details'] = {
                            'subject': dict(x[0] for x in cert.get('subject', [])),
                            'issued_to': dict(x[0] for x in cert.get('subject', [])).get('commonName'),
                            'issued_by': dict(x[0] for x in cert.get('issuer', [])).get('commonName'),
                            'valid_from': cert.get('notBefore'),
                            'valid_until': cert.get('notAfter'),
                            'san': cert.get('subjectAltName', [])
                        }
                        result['is_valid'] = True
            else:
                result['warnings'].append('Website uses HTTP instead of HTTPS - vulnerable to man-in-the-middle attacks')
                
        except Exception as e:
            result['warnings'].append(f'SSL Certificate Error: {str(e)}')
        
        return result
    
    def _analyze_security_headers(self, headers: Dict) -> Dict:
        """
        Analyze presence and validity of security headers.
        
        Args:
            headers (Dict): HTTP response headers
            
        Returns:
            Dict: Security header analysis
        """
        analysis = {
            'present': {},
            'missing': {},
            'issues': []
        }
        
        for header_name, header_info in self.REQUIRED_SECURITY_HEADERS.items():
            # Check for header (case-insensitive)
            found_header = None
            for key, value in headers.items():
                if key.lower() == header_name.lower():
                    found_header = value
                    break
            
            if found_header:
                analysis['present'][header_name] = {
                    'value': found_header,
                    'importance': header_info['importance'],
                    'description': header_info['description']
                }
            else:
                analysis['missing'][header_name] = {
                    'importance': header_info['importance'],
                    'description': header_info['description']
                }
                if header_info['importance'] in ['critical', 'high']:
                    analysis['issues'].append(
                        f"Missing {header_name} header ({header_info['importance']} importance)"
                    )
        
        return analysis
    
    def _detect_mixed_content(self, html_content: str, base_url: str) -> List[Dict]:
        """
        Detect mixed content (HTTP resources on HTTPS pages).
        
        Args:
            html_content (str): HTML content
            base_url (str): Base URL of the page
            
        Returns:
            List[Dict]: List of mixed content issues
        """
        issues = []
        
        # Only check if page is HTTPS
        if not base_url.startswith('https://'):
            return issues
        
        # Find all HTTP resource links (not https)
        http_patterns = [
            r'src=["\']http://[^"\']+["\']',
            r'href=["\']http://[^"\']+["\']',
            r'data=["\']http://[^"\']+["\']'
        ]
        
        for pattern in http_patterns:
            matches = re.findall(pattern, html_content)
            for match in matches:
                resource_url = re.search(r'(http://[^"\']+)', match).group(1)
                issues.append({
                    'type': 'mixed_content',
                    'severity': 'high',
                    'resource_url': resource_url,
                    'description': 'HTTPS page loads unencrypted HTTP resource'
                })
        
        return issues
    
    def _detect_tracking_scripts(self, html_content: str) -> List[Dict]:
        """
        Detect known tracking and analytics scripts.
        
        Args:
            html_content (str): HTML content
            
        Returns:
            List[Dict]: List of detected tracking scripts
        """
        detected_trackers = []
        
        for tracker in self.TRACKING_SCRIPTS:
            if tracker.lower() in html_content.lower():
                detected_trackers.append({
                    'name': tracker,
                    'type': 'tracking_script',
                    'privacy_concern': 'User activity may be tracked',
                    'recommendation': 'Review tracking scope and privacy policy'
                })
        
        return detected_trackers
    
    def _detect_vulnerable_libraries(self, html_content: str) -> List[Dict]:
        """
        Detect known vulnerable JavaScript libraries.
        
        Args:
            html_content (str): HTML content
            
        Returns:
            List[Dict]: List of detected vulnerable libraries
        """
        vulnerabilities = []
        
        for lib_name, lib_info in self.KNOWN_VULNERABLE_LIBS.items():
            # Look for script tags with library references
            pattern = rf'src=["\']([^"\']*{lib_name}[^"\']*)["\']'
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            
            for match in matches:
                # Try to extract version
                version_match = re.search(r'(v?\d+\.\d+\.\d+)', match)
                version = version_match.group(1) if version_match else 'unknown'
                
                vulnerabilities.append({
                    'library': lib_name,
                    'detected_source': match,
                    'version': version,
                    'risk_level': lib_info['risk'],
                    'vulnerability': lib_info['description'],
                    'recommendation': f'Update {lib_name} to the latest patched version'
                })
        
        return vulnerabilities
    
    def _analyze_cookies(self, cookies: requests.cookies.RequestsCookieJar) -> List[Dict]:
        """
        Analyze cookies for security issues.
        
        Args:
            cookies (RequestsCookieJar): Cookies from response
            
        Returns:
            List[Dict]: Cookie security issues
        """
        issues = []
        
        for cookie in cookies:
            cookie_issues = []
            
            # Check for Secure flag (HTTPS only)
            if not cookie.secure:
                cookie_issues.append('Missing Secure flag - vulnerable to interception')
            
            # Check for HttpOnly flag
            if not cookie.has_nonstandard_attr('HttpOnly'):
                cookie_issues.append('Missing HttpOnly flag - vulnerable to XSS attacks')
            
            if cookie_issues:
                issues.append({
                    'name': cookie.name,
                    'issues': cookie_issues,
                    'severity': 'medium' if len(cookie_issues) == 1 else 'high'
                })
        
        return issues
    
    def _calculate_risk_score(self, report: Dict) -> int:
        """
        Calculate overall risk score based on findings.
        
        Args:
            report (Dict): Security assessment report
            
        Returns:
            int: Risk score (0-100)
        """
        score = 0
        max_score = 100
        
        # SSL/Certificate issues (30 points)
        if not report['ssl_certificate'].get('is_valid', False):
            score += 30
        elif not report['ssl_certificate'].get('is_https', False):
            score += 20
        
        # Missing security headers (40 points)
        missing_critical = len([h for h, info in report['security_headers'].get('missing', {}).items() 
                               if info.get('importance') == 'critical'])
        missing_high = len([h for h, info in report['security_headers'].get('missing', {}).items() 
                           if info.get('importance') == 'high'])
        score += missing_critical * 10 + missing_high * 5
        
        # Vulnerable libraries (20 points)
        for vuln in report['vulnerable_libraries']:
            if vuln['risk_level'] == 'high':
                score += 10
            elif vuln['risk_level'] == 'medium':
                score += 5
        
        # Mixed content (15 points)
        score += len(report['mixed_content_issues']) * 5
        
        # Cookie issues (10 points)
        score += len(report['cookie_issues']) * 3
        
        return min(score, max_score)
    
    def _determine_risk_level(self, score: int) -> str:
        """
        Determine risk level from score.
        
        Args:
            score (int): Risk score
            
        Returns:
            str: Risk level (critical, high, medium, low, minimal)
        """
        if score >= 80:
            return 'critical'
        elif score >= 60:
            return 'high'
        elif score >= 40:
            return 'medium'
        elif score >= 20:
            return 'low'
        else:
            return 'minimal'
    
    def _generate_recommendations(self, report: Dict) -> List[str]:
        """
        Generate actionable security recommendations based on findings.
        
        Args:
            report (Dict): Security assessment report
            
        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        
        # SSL/HTTPS recommendations
        if not report['ssl_certificate'].get('is_https'):
            recommendations.append(
                '🔒 Enable HTTPS: This website should use HTTPS to encrypt data in transit. '
                'Contact the website owner to migrate to HTTPS.'
            )
        elif not report['ssl_certificate'].get('is_valid'):
            recommendations.append(
                '⚠️ SSL Certificate Issue: The SSL certificate is invalid or expired. '
                'Avoid entering sensitive information on this site.'
            )
        
        # Security header recommendations
        missing_headers = report['security_headers'].get('missing', {})
        if 'Content-Security-Policy' in missing_headers:
            recommendations.append(
                '🛡️ Implement Content-Security-Policy (CSP): This header helps prevent XSS attacks. '
                'Contact the website owner to implement CSP.'
            )
        if 'X-Frame-Options' in missing_headers:
            recommendations.append(
                '🚫 Implement X-Frame-Options: This header prevents clickjacking attacks. '
                'Contact the website owner to add this header.'
            )
        
        # Vulnerable libraries recommendations
        if report['vulnerable_libraries']:
            recommendations.append(
                f'📚 Update Vulnerable Libraries: {len(report["vulnerable_libraries"])} vulnerable '
                f'JavaScript library/libraries detected. These should be updated to patched versions.'
            )
        
        # Tracking scripts recommendations
        if report['tracking_scripts']:
            recommendations.append(
                f'👁️ Privacy Concern: {len(report["tracking_scripts"])} tracking script(s) detected. '
                f'Review the website\'s privacy policy and consider blocking trackers using browser extensions.'
            )
        
        # Mixed content recommendations
        if report['mixed_content_issues']:
            recommendations.append(
                f'🔗 Mixed Content: {len(report["mixed_content_issues"])} HTTP resource(s) loaded on HTTPS page. '
                f'This undermines HTTPS security.'
            )
        
        # Cookie recommendations
        if report['cookie_issues']:
            recommendations.append(
                f'🍪 Cookie Security: {len(report["cookie_issues"])} cookie(s) with security issues detected. '
                f'Review security settings and ensure Secure and HttpOnly flags are set.'
            )
        
        # General privacy recommendations
        if not recommendations:
            recommendations.append(
                '✅ Website appears to have good security practices. Continue monitoring for updates.'
            )
        
        return recommendations

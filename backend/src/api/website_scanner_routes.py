"""
Website Security Scanner API Endpoints

REST API endpoints for website security scanning functionality.
Provides endpoints for:
- Scanning specific websites
- Detecting active websites from browser history
- Bulk scanning of websites
- Getting scan results and recommendations
"""

from flask import Blueprint, request, jsonify
from typing import Dict, List, Optional
import logging
from datetime import datetime

# Import scanner modules
from src.scanner.website_scanner import WebsiteSecurityScanner
from src.scanner.active_website_detector import ActiveWebsiteDetector
from src.scanner.models import (
    WebsiteScanResult, BulkScanResult, RiskLevel
)

logger = logging.getLogger(__name__)

# Create Blueprint for website scanning API
website_scanner_bp = Blueprint('website_scanner', __name__, url_prefix='/api/scanner')


class WebsiteScannerAPI:
    """Main API handler for website scanning operations."""
    
    def __init__(self):
        """Initialize the API handler."""
        self.scanner = WebsiteSecurityScanner()
        self.detector = ActiveWebsiteDetector()
    
    def scan_website(self, url: str) -> Dict:
        """
        Scan a specific website for security risks.
        
        Args:
            url (str): Website URL to scan
            
        Returns:
            Dict: Scan report
        """
        logger.info(f"Starting scan for: {url}")
        report = self.scanner.scan_website(url)
        logger.info(f"Scan completed for {url} with risk level: {report['overall_risk_level']}")
        return report
    
    def get_active_websites(self, browser: Optional[str] = None, 
                           limit: int = 50) -> Dict:
        """
        Get active/recent websites from browser history.
        
        Args:
            browser (str): Specific browser to scan ('chrome', 'firefox', 'edge', 'all')
            limit (int): Maximum number of websites to return
            
        Returns:
            Dict: List of websites with metadata
        """
        logger.info(f"Detecting active websites from {browser or 'all'} browser(s)")
        websites = self.detector.get_active_websites(browser)[:limit]
        
        return {
            'total_websites': len(websites),
            'websites': websites,
            'timestamp': datetime.now().isoformat()
        }
    
    def scan_active_websites(self, browser: Optional[str] = None, 
                           limit: int = 10) -> Dict:
        """
        Scan recently active websites for security risks.
        
        Args:
            browser (str): Specific browser to scan
            limit (int): Maximum number of websites to scan
            
        Returns:
            Dict: Bulk scan results
        """
        logger.info(f"Starting bulk scan of active websites from {browser or 'all'}")
        
        # Get active websites
        websites = self.detector.get_active_websites(browser)[:limit]
        
        # Create bulk result
        bulk_result = BulkScanResult(total=len(websites))
        
        # Scan each website
        for website in websites:
            try:
                report = self.scanner.scan_website(website['url'])
                bulk_result.add_report(report)
            except Exception as e:
                logger.error(f"Error scanning {website['url']}: {str(e)}")
                bulk_result.add_error(website['url'], str(e))
        
        logger.info(f"Bulk scan completed: {bulk_result.completed}/{bulk_result.total} successful")
        return bulk_result.to_dict()
    
    def scan_multiple_websites(self, urls: List[str]) -> Dict:
        """
        Scan multiple specified websites.
        
        Args:
            urls (List[str]): List of URLs to scan
            
        Returns:
            Dict: Bulk scan results
        """
        logger.info(f"Starting bulk scan of {len(urls)} websites")
        
        bulk_result = BulkScanResult(total=len(urls))
        
        for url in urls:
            try:
                report = self.scanner.scan_website(url)
                bulk_result.add_report(report)
            except Exception as e:
                logger.error(f"Error scanning {url}: {str(e)}")
                bulk_result.add_error(url, str(e))
        
        logger.info(f"Bulk scan completed: {bulk_result.completed}/{bulk_result.total} successful")
        return bulk_result.to_dict()
    
    def get_scan_summary(self, report: Dict) -> Dict:
        """
        Get a summary of a scan report.
        
        Args:
            report (Dict): Full scan report
            
        Returns:
            Dict: Summary of findings
        """
        return {
            'url': report['url'],
            'scan_timestamp': report['scan_timestamp'],
            'is_reachable': report['is_reachable'],
            'risk_score': report['risk_score'],
            'overall_risk_level': report['overall_risk_level'],
            'issues_found': {
                'missing_security_headers': len(report['security_headers'].get('missing', {})),
                'mixed_content': len(report['mixed_content_issues']),
                'tracking_scripts': len(report['tracking_scripts']),
                'vulnerable_libraries': len(report['vulnerable_libraries']),
                'cookie_issues': len(report['cookie_issues']),
            },
            'ssl_valid': report['ssl_certificate'].get('is_valid'),
            'uses_https': report['ssl_certificate'].get('is_https'),
            'recommendations_count': len(report['recommendations'])
        }
    
    def get_risky_websites(self, websites: List[Dict], 
                          min_risk_score: int = 60) -> List[Dict]:
        """
        Filter websites by risk score.
        
        Args:
            websites (List[Dict]): List of website reports
            min_risk_score (int): Minimum risk score to include
            
        Returns:
            List[Dict]: Filtered websites sorted by risk
        """
        risky = [w for w in websites if w.get('risk_score', 0) >= min_risk_score]
        return sorted(risky, key=lambda x: x.get('risk_score', 0), reverse=True)


# Initialize API handler
api_handler = WebsiteScannerAPI()


# ============================================
# API Routes
# ============================================

@website_scanner_bp.route('/scan', methods=['POST'])
def scan_website_endpoint():
    """
    Endpoint to scan a specific website.
    
    Request body:
        {
            "url": "https://example.com"
        }
    
    Response:
        {
            "success": true,
            "data": {report},
            "timestamp": "2024-02-08T10:30:00"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': 'URL is required in request body'
            }), 400
        
        url = data['url'].strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL cannot be empty'
            }), 400
        
        report = api_handler.scan_website(url)
        
        return jsonify({
            'success': True,
            'data': report,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in scan_website_endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@website_scanner_bp.route('/scan/summary', methods=['POST'])
def scan_summary_endpoint():
    """
    Endpoint to get summary of a website scan.
    
    Request body:
        {
            "url": "https://example.com"
        }
    
    Response:
        {
            "success": true,
            "data": {summary},
            "timestamp": "2024-02-08T10:30:00"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        url = data['url'].strip()
        report = api_handler.scan_website(url)
        summary = api_handler.get_scan_summary(report)
        
        return jsonify({
            'success': True,
            'data': summary,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in scan_summary_endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@website_scanner_bp.route('/active-websites', methods=['GET'])
def get_active_websites_endpoint():
    """
    Endpoint to get active/recent websites from browser history.
    
    Query parameters:
        - browser: 'chrome', 'firefox', 'edge', or 'all' (default: all)
        - limit: Maximum number of websites (default: 50)
    
    Response:
        {
            "success": true,
            "data": {
                "total_websites": 10,
                "websites": [...],
                "timestamp": "2024-02-08T10:30:00"
            }
        }
    """
    try:
        browser = request.args.get('browser', 'all')
        limit = min(int(request.args.get('limit', 50)), 200)
        
        result = api_handler.get_active_websites(browser, limit)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_active_websites_endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@website_scanner_bp.route('/scan-active', methods=['GET'])
def scan_active_websites_endpoint():
    """
    Endpoint to scan active websites from browser history.
    
    Query parameters:
        - browser: 'chrome', 'firefox', 'edge', or 'all' (default: all)
        - limit: Maximum websites to scan (default: 10)
    
    Response:
        {
            "success": true,
            "data": {
                "summary": {
                    "total": 10,
                    "completed": 10,
                    "failed": 0,
                    "timestamp": "..."
                },
                "reports": [...]
            }
        }
    """
    try:
        browser = request.args.get('browser', 'all')
        limit = min(int(request.args.get('limit', 10)), 50)
        
        result = api_handler.scan_active_websites(browser, limit)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error in scan_active_websites_endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@website_scanner_bp.route('/scan-multiple', methods=['POST'])
def scan_multiple_websites_endpoint():
    """
    Endpoint to scan multiple specified websites.
    
    Request body:
        {
            "urls": ["https://example.com", "https://test.com"]
        }
    
    Response:
        {
            "success": true,
            "data": {
                "summary": {...},
                "reports": [...]
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({
                'success': False,
                'error': 'URLs list is required'
            }), 400
        
        urls = data['urls']
        
        if not isinstance(urls, list):
            return jsonify({
                'success': False,
                'error': 'URLs must be a list'
            }), 400
        
        if not urls:
            return jsonify({
                'success': False,
                'error': 'At least one URL is required'
            }), 400
        
        # Limit to 20 URLs per request
        urls = urls[:20]
        
        result = api_handler.scan_multiple_websites(urls)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error in scan_multiple_websites_endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@website_scanner_bp.route('/risky-websites', methods=['POST'])
def get_risky_websites_endpoint():
    """
    Endpoint to filter and get high-risk websites from scan results.
    
    Request body:
        {
            "websites": [...],
            "min_risk_score": 60
        }
    
    Response:
        {
            "success": true,
            "data": [...]
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'websites' not in data:
            return jsonify({
                'success': False,
                'error': 'Websites list is required'
            }), 400
        
        websites = data['websites']
        min_risk_score = data.get('min_risk_score', 60)
        
        risky = api_handler.get_risky_websites(websites, min_risk_score)
        
        return jsonify({
            'success': True,
            'data': risky,
            'count': len(risky)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_risky_websites_endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@website_scanner_bp.route('/health', methods=['GET'])
def health_endpoint():
    """
    Health check endpoint.
    
    Response:
        {
            "status": "healthy",
            "service": "website_scanner",
            "timestamp": "2024-02-08T10:30:00"
        }
    """
    return jsonify({
        'status': 'healthy',
        'service': 'website_scanner',
        'timestamp': datetime.now().isoformat()
    }), 200

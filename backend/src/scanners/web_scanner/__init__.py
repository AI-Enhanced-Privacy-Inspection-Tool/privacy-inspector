"""
Scanner Package

This package provides website security scanning and active website detection.

Modules:
    - website_scanner: Main security scanner class
    - active_website_detector: Browser history detection
    - models: Data models for API and internal use

Example Usage:
    >>> from src.scanner.website_scanner import WebsiteSecurityScanner
    >>> scanner = WebsiteSecurityScanner()
    >>> report = scanner.scan_website("https://example.com")
    >>> print(report['overall_risk_level'])
"""

from .website_scanner import WebsiteSecurityScanner
from .active_website_detector import ActiveWebsiteDetector
from .models import (
    WebsiteScanReport,
    Website,
    SuspiciousWebsite,
    RiskLevel
)

__all__ = [
    'WebsiteSecurityScanner',
    'ActiveWebsiteDetector',
    'WebsiteScanReport',
    'Website',
    'SuspiciousWebsite',
    'RiskLevel'
]

__version__ = '1.0.0'


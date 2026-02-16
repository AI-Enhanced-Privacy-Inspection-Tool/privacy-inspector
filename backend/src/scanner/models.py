"""
Data Models for Website Security Scanning

Defines data structures for API responses and data handling.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime


class RiskLevel(str, Enum):
    """Risk level enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"
    UNKNOWN = "unknown"
    UNREACHABLE = "unreachable"


class HeaderImportance(str, Enum):
    """Security header importance levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"


@dataclass
class SSLCertificate:
    """SSL/TLS Certificate information."""
    is_valid: bool
    is_https: bool
    certificate_details: Dict[str, Any]
    warnings: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class SecurityHeader:
    """Security header information."""
    name: str
    value: Optional[str]
    importance: str
    description: str
    present: bool
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class MixedContentIssue:
    """Mixed content (HTTP on HTTPS) issue."""
    type: str = "mixed_content"
    severity: str = "high"
    resource_url: str = ""
    description: str = "HTTPS page loads unencrypted HTTP resource"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class TrackingScript:
    """Detected tracking script information."""
    name: str
    type: str = "tracking_script"
    privacy_concern: str = "User activity may be tracked"
    recommendation: str = "Review tracking scope and privacy policy"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class VulnerableLibrary:
    """Detected vulnerable JavaScript library."""
    library: str
    detected_source: str
    version: str
    risk_level: str
    vulnerability: str
    recommendation: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class CookieIssue:
    """Cookie security issue."""
    name: str
    issues: List[str]
    severity: str = "medium"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class WebsiteScanReport:
    """Comprehensive website security scan report."""
    url: str
    scan_timestamp: str
    is_reachable: bool
    ssl_certificate: Dict[str, Any]
    security_headers: Dict[str, Any]
    mixed_content_issues: List[Dict[str, Any]]
    tracking_scripts: List[Dict[str, Any]]
    vulnerable_libraries: List[Dict[str, Any]]
    cookie_issues: List[Dict[str, Any]]
    risk_score: int
    overall_risk_level: str
    recommendations: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the report."""
        return {
            'url': self.url,
            'scan_timestamp': self.scan_timestamp,
            'is_reachable': self.is_reachable,
            'risk_score': self.risk_score,
            'overall_risk_level': self.overall_risk_level,
            'issues_found': {
                'missing_security_headers': len(self.security_headers.get('missing', {})),
                'mixed_content': len(self.mixed_content_issues),
                'tracking_scripts': len(self.tracking_scripts),
                'vulnerable_libraries': len(self.vulnerable_libraries),
                'cookie_issues': len(self.cookie_issues),
            },
            'recommendations_count': len(self.recommendations)
        }


@dataclass
class Website:
    """Website information from browser data."""
    url: str
    title: str
    last_visit: str
    source: str
    browser: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class SuspiciousWebsite:
    """Suspicious website information."""
    url: str
    domain: str
    browser: str
    last_visit: str
    reasons: List[str]
    risk_level: str = "high"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class WebsiteScanResult:
    """Result container for website scanning operations."""
    
    def __init__(self, success: bool, data: Any = None, error: Optional[str] = None):
        """
        Initialize scan result.
        
        Args:
            success (bool): Whether operation was successful
            data (Any): Result data
            error (str): Error message if operation failed
        """
        self.success = success
        self.data = data
        self.error = error
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'data': self.data,
            'error': self.error,
            'timestamp': self.timestamp
        }


class BulkScanResult:
    """Result container for bulk website scanning."""
    
    def __init__(self, total: int = 0, completed: int = 0, failed: int = 0):
        """
        Initialize bulk scan result.
        
        Args:
            total (int): Total websites to scan
            completed (int): Successfully scanned websites
            failed (int): Failed scans
        """
        self.total = total
        self.completed = completed
        self.failed = failed
        self.reports: List[Dict[str, Any]] = []
        self.timestamp = datetime.now().isoformat()
    
    def add_report(self, report: Dict[str, Any]) -> None:
        """Add a scan report."""
        self.reports.append(report)
        self.completed += 1
    
    def add_error(self, url: str, error: str) -> None:
        """Add a failed scan."""
        self.reports.append({
            'url': url,
            'error': error,
            'is_reachable': False
        })
        self.failed += 1
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'summary': {
                'total': self.total,
                'completed': self.completed,
                'failed': self.failed,
                'timestamp': self.timestamp
            },
            'reports': self.reports
        }

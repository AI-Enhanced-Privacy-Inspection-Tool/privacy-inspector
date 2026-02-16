"""
Example Usage and Testing Script for Website Security Scanner

This script demonstrates how to use the website security scanner
functionality for scanning specific websites and detecting active websites.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from src.scanner.website_scanner import WebsiteSecurityScanner
from src.scanner.active_website_detector import ActiveWebsiteDetector
import json


def print_separator(title: str = ""):
    """Print a formatted separator line."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'-'*60}\n")


def print_report_summary(report: dict):
    """Print a formatted summary of the scan report."""
    print(f"URL: {report['url']}")
    print(f"Scan Time: {report['scan_timestamp']}")
    print(f"Reachable: {'✓' if report['is_reachable'] else '✗'}")
    print(f"Risk Score: {report['risk_score']}/100")
    print(f"Risk Level: {report['overall_risk_level'].upper()}")
    
    print("\nSecurity Issues Found:")
    print(f"  • Missing Security Headers: {len(report['security_headers'].get('missing', {}))}")
    print(f"  • Mixed Content: {len(report['mixed_content_issues'])}")
    print(f"  • Tracking Scripts: {len(report['tracking_scripts'])}")
    print(f"  • Vulnerable Libraries: {len(report['vulnerable_libraries'])}")
    print(f"  • Cookie Issues: {len(report['cookie_issues'])}")
    
    print(f"\nSSL/HTTPS Status:")
    ssl_info = report['ssl_certificate']
    print(f"  • Uses HTTPS: {'✓' if ssl_info.get('is_https') else '✗'}")
    print(f"  • Valid Certificate: {'✓' if ssl_info.get('is_valid') else '✗'}")
    
    print(f"\nRecommendations: {len(report['recommendations'])}")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")


def example_1_scan_single_website():
    """Example 1: Scan a single website."""
    print_separator("Example 1: Scan Single Website")
    
    scanner = WebsiteSecurityScanner()
    
    # Scan a website
    url = "https://example.com"
    print(f"Scanning {url}...\n")
    
    report = scanner.scan_website(url)
    print_report_summary(report)


def example_2_scan_multiple_websites():
    """Example 2: Scan multiple websites."""
    print_separator("Example 2: Scan Multiple Websites")
    
    scanner = WebsiteSecurityScanner()
    
    urls = [
        "https://google.com",
        "https://github.com",
        "https://stackexchange.com",
    ]
    
    reports = []
    for url in urls:
        print(f"Scanning {url}...")
        report = scanner.scan_website(url)
        reports.append(report)
        print(f"  Risk Level: {report['overall_risk_level'].upper()}")
        print()
    
    # Summary of all scans
    print_separator("Scan Results Summary")
    
    # Sort by risk score
    sorted_reports = sorted(reports, key=lambda x: x['risk_score'], reverse=True)
    
    print(f"{'Website':<30} {'Risk Level':<15} {'Risk Score':<12}")
    print("-" * 60)
    for report in sorted_reports:
        domain = report['url'].replace('https://', '').replace('http://', '').split('/')[0]
        risk_level = report['overall_risk_level'].upper()
        risk_score = report['risk_score']
        print(f"{domain:<30} {risk_level:<15} {risk_score:<12}")


def example_3_detect_active_websites():
    """Example 3: Detect active/recent websites from browser."""
    print_separator("Example 3: Detect Active Websites from Browser")
    
    detector = ActiveWebsiteDetector()
    
    print("Detecting recently visited websites from Chrome, Firefox, and Edge...\n")
    
    websites = detector.get_active_websites(browser='all', limit=10)
    
    print(f"Found {len(websites)} recently visited websites:\n")
    print(f"{'Website':<30} {'Browser':<15} {'Last Visit':<25}")
    print("-" * 70)
    
    for i, site in enumerate(websites, 1):
        domain = site['url'].replace('https://', '').replace('http://', '').split('/')[0][:28]
        browser = site.get('browser', 'Unknown')
        last_visit = site.get('last_visit', 'Unknown')[:19]
        print(f"{i}. {domain:<28} {browser:<15} {last_visit:<25}")


def example_4_scan_active_websites():
    """Example 4: Scan active websites for security issues."""
    print_separator("Example 4: Scan Active Websites for Security Issues")
    
    scanner = WebsiteSecurityScanner()
    detector = ActiveWebsiteDetector()
    
    print("Getting active websites from Chrome...\n")
    websites = detector.get_active_websites(browser='chrome', limit=5)
    
    if not websites:
        print("No active websites found in Chrome history.")
        return
    
    print(f"Scanning {len(websites)} websites...\n")
    
    high_risk_count = 0
    for i, website in enumerate(websites, 1):
        url = website['url']
        print(f"[{i}/{len(websites)}] Scanning {url}...")
        
        try:
            report = scanner.scan_website(url)
            risk_level = report['overall_risk_level']
            risk_score = report['risk_score']
            
            print(f"      Risk Level: {risk_level.upper()}, Score: {risk_score}/100")
            
            if risk_score >= 60:
                high_risk_count += 1
        except Exception as e:
            print(f"      Error: {str(e)}")
        print()
    
    print(f"Summary: {high_risk_count}/{len(websites)} websites have high risk scores (>60)")


def example_5_detect_suspicious_websites():
    """Example 5: Detect suspicious websites in browser history."""
    print_separator("Example 5: Detect Suspicious Websites")
    
    detector = ActiveWebsiteDetector()
    
    print("Getting all websites from browser history...\n")
    websites = detector.get_active_websites(browser='all', limit=50)
    
    if not websites:
        print("No websites found in browser history.")
        return
    
    print(f"Analyzing {len(websites)} websites for suspicious patterns...\n")
    
    suspicious = detector.get_suspicious_websites(websites)
    
    if suspicious:
        print(f"Found {len(suspicious)} potentially suspicious website(s):\n")
        for site in suspicious:
            print(f"URL: {site['url']}")
            print(f"Domain: {site['domain']}")
            print(f"Risk Level: {site['risk_level'].upper()}")
            print(f"Reasons:")
            for reason in site['reasons']:
                print(f"  • {reason}")
            print()
    else:
        print("No suspicious websites detected in your browser history.")


def example_6_detailed_security_analysis():
    """Example 6: Detailed security analysis of a specific website."""
    print_separator("Example 6: Detailed Security Analysis")
    
    scanner = WebsiteSecurityScanner()
    url = "https://example.com"
    
    print(f"Performing detailed security analysis of {url}...\n")
    
    report = scanner.scan_website(url)
    
    # Full report
    print_report_summary(report)
    
    # Missing security headers detail
    if report['security_headers'].get('missing'):
        print_separator("Missing Security Headers")
        for header, info in report['security_headers']['missing'].items():
            importance = info.get('importance', 'unknown').upper()
            description = info.get('description', '')
            print(f"• {header} [{importance}]")
            print(f"  {description}\n")
    
    # Vulnerable libraries detail
    if report['vulnerable_libraries']:
        print_separator("Vulnerable JavaScript Libraries")
        for lib in report['vulnerable_libraries']:
            print(f"• {lib['library']} ({lib['version']})")
            print(f"  Vulnerability: {lib['vulnerability']}")
            print(f"  Risk Level: {lib['risk_level'].upper()}")
            print(f"  Source: {lib['detected_source']}\n")
    
    # Tracking scripts detail
    if report['tracking_scripts']:
        print_separator("Tracking Scripts")
        for tracker in report['tracking_scripts']:
            print(f"• {tracker['name']}")
            print(f"  Privacy Concern: {tracker['privacy_concern']}\n")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("  Website Security Scanner - Usage Examples")
    print("="*60)
    
    try:
        # Run examples
        example_1_scan_single_website()
        example_2_scan_multiple_websites()
        
        print_separator("Checking Browser History Access")
        print("Note: The following examples scan websites from your browser history.")
        print("Make sure you have Chrome, Firefox, or Edge installed with history data.\n")
        
        try:
            example_3_detect_active_websites()
        except Exception as e:
            print(f"Could not access browser history: {e}")
        
        try:
            example_4_scan_active_websites()
        except Exception as e:
            print(f"Could not scan active websites: {e}")
        
        try:
            example_5_detect_suspicious_websites()
        except Exception as e:
            print(f"Could not detect suspicious websites: {e}")
        
        example_6_detailed_security_analysis()
        
        print_separator()
        print("✓ All examples completed!\n")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

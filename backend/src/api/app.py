from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

import config.settings as settings
from src.ai_analysis import AIAnalysisRequest, AIAnalysisResponse, PrivacyDataItem, DataType, analyzer
from src.scanners.app_scanner.scanner import scan_app_files
from src.scanners.web_scanner.website_scanner import WebsiteSecurityScanner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Privacy Inspector API",
    description="AI-powered privacy data analysis for desktop apps and website security scanning",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scanner
scanner = WebsiteSecurityScanner()

class WebsiteScanRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {
        "name": "Privacy Inspector API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "gemini_configured": bool(settings.GOOGLE_API_KEY),
        "scanner_enabled": True
    }


@app.post("/analyze", response_model=AIAnalysisResponse)
async def analyze(request: AIAnalysisRequest):
    try:
        result = analyzer.analyze_items(request.data_items)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/scan/desktop", response_model=AIAnalysisResponse)
async def scan_desktop():
    "Run the local desktop app scanner and analyze formatted results with AI"

    try:
        counts, all_findings, compacted_results, formatted_results = scan_app_files()

        print("Scanning triggered!")

        data_items = []

        # Use formatted_results for AI analysis (includes actual data previews)
        for app_name, findings in formatted_results.get("apps", {}).items():
            for finding in findings:
                item = PrivacyDataItem(
                    name=f"{app_name}:{finding['category']}",
                    value=finding['value_preview'],
                    data_type=DataType.OTHER,
                    domain=app_name,
                    metadata={
                        "app_name": app_name,
                        "category": finding['category'],
                        "file_path": finding['file_path'],
                        "field_path": finding['field_path'],
                        "detection_method": finding['detection_method'],
                        "confidence": finding['confidence']
                    },
                )
                data_items.append(item)

        result = analyzer.analyze_items(data_items)

        # Attach scanner context with formatted results at the top level
        result.summary.setdefault("scanner", {})
        result.summary["scanner"]["file_counts"] = {k: int(v) for k, v in counts.items()}
        result.summary["scanner"]["formatted_results"] = formatted_results

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Desktop scan failed: {str(e)}")


@app.post("/scan/website", response_model=AIAnalysisResponse)
async def scan_website(request: WebsiteScanRequest):
    """Scan a website for security and privacy risks with AI-powered analysis"""
    try:
        url = request.url.strip()
        if not url:
            raise HTTPException(status_code=400, detail="URL cannot be empty")
        
        logger.info(f"Starting scan for: {url}")
        report = scanner.scan_website(url)
        logger.info(f"Scan completed for {url} with risk level: {report['overall_risk_level']}")
        
        data_items = []
        
        # Convert all findings to PrivacyDataItem objects
        for tracking in report.get('tracking_scripts', []):
            data_items.append(PrivacyDataItem(
                name=f"Tracking Script: {tracking.get('name', 'Unknown')}", 
                value=f"Risk: {tracking.get('risk', 'medium')} - {tracking.get('url', '')}",
                data_type=DataType.OTHER, domain=url,
                metadata={"type": "tracking", **tracking}
            ))
        
        for lib in report.get('vulnerable_libraries', []):
            data_items.append(PrivacyDataItem(
                name=f"Vulnerable Library: {lib.get('library', 'Unknown')}", 
                value=f"Version {lib.get('version', 'Unknown')} - Risk: {lib.get('risk', 'Unknown')} - {lib.get('description', '')}",
                data_type=DataType.OTHER, domain=url,
                metadata={"type": "vulnerability", **lib}
            ))
        
        for cookie in report.get('cookie_issues', []):
            issues = ', '.join(cookie.get('issues', []))
            data_items.append(PrivacyDataItem(
                name=f"Cookie Issue: {cookie.get('name', 'Unknown')}", 
                value=f"Issues: {issues}",
                data_type=DataType.OTHER, domain=url,
                metadata={"type": "cookie", **cookie}
            ))
        
        # Add missing security headers
        for header_name, header_info in report.get('security_headers', {}).get('missing', {}).items():
            data_items.append(PrivacyDataItem(
                name=f"Security Issue: Missing {header_name}",
                value=f"{header_info.get('importance', 'medium').upper()} risk - {header_info.get('description', '')}",
                data_type=DataType.OTHER, domain=url,
                metadata={"type": "security_header", "header": header_name, "importance": header_info.get('importance', 'medium')}
            ))
        
        # Add mixed content issues
        for mixed in report.get('mixed_content_issues', []):
            data_items.append(PrivacyDataItem(
                name="MixedContent",
                value=mixed.get('url', ''),
                data_type=DataType.OTHER, domain=url,
                metadata={"type": "mixed_content", "resource_type": mixed.get('type', 'unknown')}
            ))
        
        logger.info(f"Created {len(data_items)} data items for AI analysis")
        result = analyzer.analyze_items(data_items)
        
        # Attach scanner context
        result.summary.setdefault("scanner", {})
        result.summary["scanner"]["website_report"] = report
        
        return result
        
    except Exception as e:
        logger.error(f"Error scanning website: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Website scan failed: {str(e)}")
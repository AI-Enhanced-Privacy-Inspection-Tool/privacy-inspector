from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from src.scanner.website_scanner import WebsiteSecurityScanner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Privacy Inspector API",
    description="AI-powered privacy data analysis and website security scanning",
    version="1.0.0",
)

# Add CORS middleware
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
    """Root endpoint."""
    return {
        "name": "Privacy Inspector API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "scanner_enabled": True
    }


@app.post("/scan/website")
async def scan_website(request: WebsiteScanRequest):
    """
    Scan a website for security and privacy risks.
    
    Args:
        request: WebsiteScanRequest with URL to scan
        
    Returns:
        Scan report with security findings
    """
    try:
        url = request.url.strip()
        
        if not url:
            raise HTTPException(status_code=400, detail="URL cannot be empty")
        
        logger.info(f"Starting scan for: {url}")
        report = scanner.scan_website(url)
        logger.info(f"Scan completed for {url} with risk level: {report['overall_risk_level']}")
        
        return {
            "success": True,
            "data": report
        }
        
    except Exception as e:
        logger.error(f"Error scanning website: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Website scan failed: {str(e)}")

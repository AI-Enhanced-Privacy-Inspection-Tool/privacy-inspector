from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import config.settings as settings
from src.ai_analysis import AIAnalysisRequest, AIAnalysisResponse, PrivacyDataItem, DataType, analyzer
from src.scanners.app_scanner.scanner import scan_app_files

app = FastAPI(
    title="Privacy Inspector API",
    description="AI-powered privacy data analysis",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        "gemini_configured": bool(settings.GOOGLE_API_KEY)
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
    "Run the local desktop app scanner and analyze compact results with AI"

    try:
        counts, all_findings, compacted_results, formatted_results = scan_app_files()

        print("Scanning triggered!")

        data_items = []

        for app_name, categories in compacted_results.items():
            for category in categories:
                item = PrivacyDataItem(
                    name=f"{app_name}:{category}",
                    value=f"Application '{app_name}' stores data of category '{category}' on the local machine.",
                    data_type=DataType.OTHER,
                    domain=app_name,
                    metadata={"app_name": app_name, "category": category},
                )
                data_items.append(item)

        result = analyzer.analyze_items(data_items)

        # Attach raw scanner context into the summary for frontend use
        result.summary.setdefault("scanner", {})
        result.summary["scanner"]["file_counts"] = {k: int(v) for k, v in counts.items()}
        result.summary["scanner"]["formatted_results"] = formatted_results

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Desktop scan failed: {str(e)}")
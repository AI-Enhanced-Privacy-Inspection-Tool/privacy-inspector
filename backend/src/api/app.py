from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import config.settings as settings
from src.ai_analysis import AIAnalysisRequest, AIAnalysisResponse, analyzer

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

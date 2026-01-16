# AI-Enhanced Privacy Inspection Tool

A local tool that scans your computer for privacy-relevant data stored by browsers and applications, uses AI to analyze and classify findings, and provides actionable recommendations.

## Features

- Scans browser storage (cookies, local storage, cache) and app configs
- AI-powered data sensitivity classification and PII detection
- Risk assessment with actionable suggestions
- Web interface for insights and recommendations

## Project Structure

```
privacy-inspector/
├── backend/                    # Python backend
│   ├── src/
│   │   ├── scanner/           # Data scanning and extraction
│   │   ├── ai_analysis/       # AI classification and detection
│   │   ├── risk_assessment/   # Risk scoring and recommendations
│   │   └── api/               # REST API endpoints
│   ├── config/
│   ├── tests/
│   └── requirements.txt
│
└── frontend/                   # Web interface
```

## Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
# Setup 
```

## Privacy

This tool runs entirely locally. No data is sent to external servers.
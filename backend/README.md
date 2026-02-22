# Backend API

Python-based backend for privacy analysis using Google Gemini AI

## Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:
```
GOOGLE_API_KEY=your_api_key_here
```

## Run

```bash
uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: http://localhost:8000

## API Endpoints

### GET /
Basic API info.

### GET /health
Check if server is running and whether `GOOGLE_API_KEY` is configured.

### POST /analyze
Generic AI analysis endpoint. Accepts a JSON body with `data_items` (list of privacy data items) and returns an `AIAnalysisResponse`.

### POST /scan/desktop
Run the local desktop scanner and AI analysis in one step.

- Scans Windows app data folders for JSON/text/SQLite files
- Builds a compact map of `app -> [categories]`
- Sends synthetic items into Gemini for risk analysis
- Returns an `AIAnalysisResponse` with:
	- `analyzed_items`: one per `(app, category)`
	- `summary` including counts and risk breakdown
	- `summary.scanner.file_counts` and `summary.scanner.compact_results`

### POST /scan/website
Scan websites for privacy-related data and perform AI analysis.
- Scans websites for privacy-related data in HTML/JavaScript
- Extracts tracking scripts, cookies, and data collection mechanisms
- Sends findings into Gemini for risk analysis
- Returns an `AIAnalysisResponse` with:
	- `analyzed_items`: one per detected privacy concern
	- `summary` including counts and risk breakdown
	- `summary.scanner.domains` and `summary.scanner.trackers`

## Testing

Postman or visit http://localhost:8000/docs for interactive API docs

## Structure

```
backend/
├── config/settings.py
├── src/
│   ├── ai_analysis/
│   │   ├── models.py
│   │   ├── prompts.py
│   │   └── service.py
│   ├── scanners/
│   │   ├── app_scanner/
│   │   │   ├── scanner.py
│   │   │   ├── main.py
│   │   │   ├── discovery/
│   │   │   ├── extraction/
│   │   │   └── detection/
│   │   └── website_scanner/
│   │       ├── active_website_detector.py
│   │       ├── models.py
│   │       └── website_scanner.py
│   └── api/app.py
└── requirements.txt
```

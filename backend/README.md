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

### GET /health
Check if server is running

### POST /analyze
Analyze privacy data

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
│   └── api/app.py
└── requirements.txt
```

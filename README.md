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
│   ├── config/                # Configuration files
│   ├── tests/                 # Unit and integration tests
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend setup guide
│
├── frontend/                   # Web interface
│   ├── src/
│   ├── public/
│   ├── package.json           # Node dependencies
│   └── README.md              # Frontend setup guide
│
├── docs/                       # Documentation
├── .gitignore
├── LICENSE
└── README.md                   # Main project README
```

## Setup

For detailed setup instructions, please refer to the README files in the respective directories:

- **Backend Setup**: See `/backend/README.md`
- **Frontend Setup**: See `/frontend/README.md`

## Privacy

This tool runs entirely locally. No data is sent to external servers.
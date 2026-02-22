# Privacy Inspector - Frontend

A React + TypeScript + Vite application for the AI-Enhanced Privacy Inspection Tool. This frontend provides a user interface for analyzing and managing privacy settings across digital services.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **ESLint** - Code quality and consistency
- **Tailwind CSS**

## Prerequisites

- Node.js 16+ and npm or yarn
- Git

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AI-Enhanced-Privacy-Inspection-Tool/privacy-inspector.git
   cd privacy-inspector/frontend/Privacy-Inspector
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Usage

After starting the dev server, open your browser to `http://localhost:5173` and use the interface to analyze privacy settings.

## UI Sections

- **Local Scan**: triggers desktop scan and shows AI-analyzed privacy findings
- **Website Scan**: shows website vulnerability and cookie/header insights

## Structure

```text
frontend/Privacy-Inspector/
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   ├── index.css
│   ├── components/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── LoadingScan.tsx
│   │   ├── LocalAiInsight.tsx
│   │   └── WebsiteAiInsight.tsx
│   └── pages/
│       ├── Dashboard.tsx
│       ├── ScanResult.tsx
│       └── WebsiteScan.tsx
└── README.md
```

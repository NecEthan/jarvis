# Jarvis — Personal AI Assistant

A monorepo containing a Next.js frontend, FastAPI/LangGraph AI backend, and shared utilities.

## Project Structure

```
jarvis/
├── apps/
│   ├── web/                  # Next.js frontend + API routes
│   │   ├── app/
│   │   │   ├── page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── api/
│   │   │       ├── agent/route.ts
│   │   │       ├── tts/route.ts
│   │   │       └── sonos/
│   │   │           ├── play/route.ts
│   │   │           └── control/route.ts
│   │   ├── lib/
│   │   │   └── sonos.ts
│   │   └── public/audio/
│   └── ai/                   # FastAPI + LangGraph service
│       └── app/
│           ├── main.py
│           ├── graph.py
│           └── nodes/
│               ├── intent.py
│               ├── context.py
│               ├── decision.py
│               └── output.py
└── packages/
    └── shared/               # Shared TypeScript types
        └── index.ts
```

## Prerequisites

- Node.js 20+
- Python 3.11+

## Install Dependencies

### JavaScript (root — installs all workspaces)

```bash
npm install
```

### Python (FastAPI service)

```bash
cd apps/ai
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Variables

Copy the example env files and fill in values:

```bash
cp apps/web/.env.example apps/web/.env.local
cp apps/ai/.env.example apps/ai/.env
```

## Running Dev Servers

### All services (requires `concurrently`)

```bash
npm run dev
```

### Web only

```bash
npm run dev:web
```

### AI service only

```bash
npm run dev:ai
```

| Service | URL                   |
|---------|-----------------------|
| Web     | http://localhost:3000 |
| AI API  | http://localhost:8000 |
| API docs| http://localhost:8000/docs |

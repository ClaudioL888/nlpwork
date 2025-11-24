# Digital Empathy Platform

This repository hosts the backend/ frontend code for the Digital Empathy Platform. The initial milestone covers provisioning a FastAPI backend scaffold with configuration, logging, and persistence primitives that future feature work can build on.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
alembic upgrade head
uvicorn src.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Docker Compose stack
docker compose -f deploy/docker-compose.yml up --build

# Tests
pytest tests/unit tests/services tests/api tests/integration
(cd frontend && npm run test:e2e)

# Performance (requires API running)
locust -f tests/perf/locustfile.py
```

The application defaults to using SQLite (async) for local development and exposes a `/health` endpoint for smoke tests.

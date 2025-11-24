# Operations Runbook

## Environments
- **Local dev**: FastAPI at `http://localhost:8000`, Vite dev server `http://localhost:5173`.
- **Compose stack**: `docker-compose -f deploy/docker-compose.yml up --build` spins up API, Postgres, Redis, frontend (Nginx), Prometheus, Grafana.

## Health and Monitoring
- Health probe: `GET /health` (no API key required).
- Metrics: `GET /metrics` (Prometheus format). Compose configuration scrapes this endpoint.
- Grafana default credentials: `admin/admin`. Add Prometheus (`http://prometheus:9090`) as a data source.

### Alerts
Prometheus config includes a scrape job only; add alert rules under `deploy/prometheus.yml` if needed. Recommended alerts:
- High request latency (`dep_request_latency_seconds` histogram).
- Elevated 5xx rate (`dep_requests_total{status="500"}`).
- Chat rate-limit saturation.

## Security
- All non-excluded routes require the API key via `x-api-key` header. Key value comes from `APP_SECURITY__API_KEY` (default in `.env.example`).
- Global rate limit defaults to 60 req/min/IP. Adjust via settings `SECURITY__RATE_LIMIT_REQUESTS` and `SECURITY__RATE_LIMIT_WINDOW_SECONDS`.
- WebSocket chat still enforces per-user rate limiting inside `ChatGateway`.

## Deployment
1. Ensure `.env` is populated with production secrets (DB URL, API key, Redis, observability endpoints).
2. Run Alembic migrations before deploying new versions: `alembic upgrade head` (container command `docker compose exec api alembic upgrade head`).
3. Build/push backend + frontend images, update compose/stack references, and redeploy (e.g., `docker compose pull && docker compose up -d`).
4. Verify:
   - `curl http://<host>:8000/health`
   - `curl -H "x-api-key: <key>" http://<host>:8000/api/analyze_text -d '{"text":"hi"}'`
   - Prometheus scrape targets healthy, Grafana dashboard loads.

## Rollback
- Keep previous container images tagged (e.g., `api:previous`).
- To rollback: `docker compose -f deploy/docker-compose.yml up -d api=<previous-tag>`.
- For DB issues, use Postgres PITR / backups stored in `db_data` volume snapshots.

## Troubleshooting
- **401 Unauthorized**: ensure `x-api-key` header matches backend setting or path is added to excluded list (`src/security/auth.py`).
- **429 Rate limit**: confirm rate window or add service account IP to `excluded_paths` if necessary.
- **Metrics missing**: confirm `/metrics` reachable without API key and Prometheus config references correct target.
- **High latency**: inspect `dep_request_latency_seconds` histogram, enable debug log level via `OBSERVABILITY__LOG_LEVEL=DEBUG`.

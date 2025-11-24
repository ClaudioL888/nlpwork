from __future__ import annotations

import time
from typing import Iterable

from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

REQUEST_COUNT = Counter(
    "dep_requests_total",
    "Total HTTP requests",
    labelnames=("method", "path", "status"),
)
REQUEST_LATENCY = Histogram(
    "dep_request_latency_seconds",
    "HTTP request latency",
    labelnames=("method", "path"),
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Emit Prometheus metrics for HTTP traffic."""

    def __init__(self, app, ignored_paths: Iterable[str] | None = None) -> None:  # type: ignore[override]
        super().__init__(app)
        self.ignored_paths = set(ignored_paths or [])

    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        if request.scope.get("type") != "http" or request.url.path in self.ignored_paths:
            return await call_next(request)

        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
        REQUEST_LATENCY.labels(request.method, request.url.path).observe(duration)
        return response

from __future__ import annotations

import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.core.logging.config import get_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Structured request logging for HTTP requests."""

    def __init__(self, app, service_name: str = "api") -> None:  # type: ignore[override]
        super().__init__(app)
        self.logger = get_logger("logging_middleware")
        self.service_name = service_name

    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        if request.scope.get("type") != "http":
            return await call_next(request)

        request_id = request.headers.get("x-request-id", uuid.uuid4().hex)
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as exc:  # pragma: no cover - logging path
            duration_ms = (time.perf_counter() - start) * 1000
            self.logger.exception(
                "http.request.error",
                service=self.service_name,
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                duration_ms=round(duration_ms, 2),
                client_ip=request.client.host if request.client else "unknown",
            )
            raise exc

        duration_ms = (time.perf_counter() - start) * 1000
        response.headers["x-request-id"] = request_id
        self.logger.info(
            "http.request",
            service=self.service_name,
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
            client_ip=request.client.host if request.client else "unknown",
        )
        return response

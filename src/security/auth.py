from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Iterable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.config.settings import get_settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_paths: Iterable[str] | None = None) -> None:  # type: ignore[override]
        super().__init__(app)
        self.settings = get_settings()
        self.excluded_paths = set(excluded_paths or [])

    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        if request.scope.get("type") != "http" or request.url.path in self.excluded_paths:
            return await call_next(request)

        expected = self.settings.security.api_key
        incoming = request.headers.get("x-api-key")
        if not expected or incoming != expected:
            return JSONResponse({"detail": "Invalid API key"}, status_code=401)
        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        *,
        max_requests: int,
        window_seconds: int,
        excluded_paths: Iterable[str] | None = None,
    ) -> None:  # type: ignore[override]
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.excluded_paths = set(excluded_paths or [])
        self._requests: defaultdict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        if request.scope.get("type") != "http" or request.url.path in self.excluded_paths:
            return await call_next(request)

        identity = request.client.host if request.client else "anonymous"
        now = time.time()
        window_start = now - self.window_seconds
        bucket = self._requests[identity]
        while bucket and bucket[0] < window_start:
            bucket.popleft()
        if len(bucket) >= self.max_requests:
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
        bucket.append(now)
        return await call_next(request)

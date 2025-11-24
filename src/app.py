from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from src.api.routers import register_routes
from src.config.settings import AppSettings, get_settings
from src.core.logging.config import configure_logging, get_logger
from src.middleware.logging import LoggingMiddleware
from src.middleware.metrics import MetricsMiddleware
from src.security.auth import APIKeyMiddleware, RateLimitMiddleware


def create_app(settings: AppSettings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings.observability.log_level)
    logger = get_logger(__name__)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info(
            "app.startup",
            environment=settings.app_env,
            api_prefix=settings.api_prefix,
        )
        yield
        logger.info("app.shutdown")

    app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.security.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(LoggingMiddleware, service_name="dep-api")
    app.add_middleware(MetricsMiddleware, ignored_paths={"/metrics"})

    excluded_paths = {"/health", "/metrics", "/docs", "/openapi.json", "/redoc"}
    app.add_middleware(APIKeyMiddleware, excluded_paths=excluded_paths | {"/"})
    app.add_middleware(
        RateLimitMiddleware,
        max_requests=settings.security.rate_limit_requests,
        window_seconds=settings.security.rate_limit_window_seconds,
        excluded_paths=excluded_paths,
    )

    register_routes(app)
    app.mount("/metrics", make_asgi_app())

    return app


settings = get_settings()
app = create_app(settings)

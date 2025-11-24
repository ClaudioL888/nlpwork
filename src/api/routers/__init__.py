from fastapi import FastAPI

from .health import router as health_router
from .analyze import router as analyze_router
from .filter import router as filter_router
from .event import router as event_router
from .search import router as search_router
from .chat import router as chat_router

__all__ = ["register_routes"]


def register_routes(app: FastAPI) -> None:
    app.include_router(health_router, tags=["health"])
    app.include_router(analyze_router, tags=["analysis"])
    app.include_router(filter_router, tags=["filtering"])
    app.include_router(event_router, tags=["events"])
    app.include_router(search_router, tags=["search"])
    app.include_router(chat_router, tags=["chat"])

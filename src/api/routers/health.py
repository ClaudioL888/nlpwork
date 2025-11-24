from fastapi import APIRouter

from src.config.settings import get_settings

router = APIRouter()


@router.get("/health", summary="Service health probe")
async def healthcheck() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env,
    }

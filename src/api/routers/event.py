from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.event import EventRequest, EventInsight
from src.services.event_analyzer import EventAnalyzerService, get_event_analyzer_service

router = APIRouter(prefix="/api")


@router.post(
    "/analyze_event",
    response_model=EventInsight,
    summary="Aggregate event signals for dashboard",
)
async def analyze_event_endpoint(
    payload: EventRequest,
    service: EventAnalyzerService = Depends(get_event_analyzer_service),
) -> EventInsight:
    if not payload.keyword.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Keyword is required")

    return await service.analyze_event(payload.keyword.strip(), payload.hours)

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from src.schemas.search import SearchRequest, SearchResponse
from src.services.search import SearchService, get_search_service

router = APIRouter(prefix="/api")


@router.post("/search", response_model=SearchResponse)
async def search_events(
    payload: SearchRequest,
    service: SearchService = Depends(get_search_service),
) -> SearchResponse:
    if not payload.keyword.strip():
        raise HTTPException(status_code=422, detail="Keyword required")
    return await service.search(payload)

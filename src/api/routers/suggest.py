from __future__ import annotations

from fastapi import APIRouter, Depends

from src.schemas.suggest import KeywordSuggestRequest, KeywordSuggestResponse
from src.services.keyword_suggest import KeywordSuggestService, get_keyword_suggest_service

router = APIRouter(prefix="/api")


@router.post("/suggest_keywords", response_model=KeywordSuggestResponse, summary="Suggest event keywords via LLM")
async def suggest_keywords(
    payload: KeywordSuggestRequest,
    service: KeywordSuggestService = Depends(get_keyword_suggest_service),
) -> KeywordSuggestResponse:
    keywords = service.suggest_keywords(payload.texts, payload.max_keywords)
    return KeywordSuggestResponse(keywords=keywords)

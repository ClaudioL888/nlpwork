from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.filter import FilterRequest, FilterResponse, FilterDecision, FilterEvidence
from src.services.filter import FilterService, get_filter_service

router = APIRouter(prefix="/api")


@router.post(
    "/filter",
    response_model=FilterResponse,
    summary="Filter text using rules + model signals",
)
async def filter_endpoint(
    payload: FilterRequest,
    service: FilterService = Depends(get_filter_service),
) -> FilterResponse:
    if not payload.text.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Text is empty")

    decision, allow, matches, analyzer_result = await service.filter_text(payload.text)

    evidence = [
        FilterEvidence(**match.model_dump())
        for match in matches
    ]
    return FilterResponse.from_decision(decision, allow, evidence, analyzer_result)

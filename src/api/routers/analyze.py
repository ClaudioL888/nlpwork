from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.analyze import AnalyzeTextRequest, AnalyzeTextResponse
from src.services.analyzer import AnalyzerService, get_analyzer_service

router = APIRouter(prefix="/api")


@router.post(
    "/analyze_text",
    response_model=AnalyzeTextResponse,
    summary="Analyze a single text for sentiment/empathy/crisis",
)
async def analyze_text_endpoint(
    payload: AnalyzeTextRequest,
    service: AnalyzerService = Depends(get_analyzer_service),
) -> AnalyzeTextResponse:
    if not payload.text.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Text is empty")

    result = await service.analyze_text(payload.text)
    return AnalyzeTextResponse.from_result(result)

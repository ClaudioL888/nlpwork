from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=128)
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=50)
    sort: str = Field("risk", pattern="^(risk|heat)$")


class SearchResultItem(BaseModel):
    keyword: str
    window_start: datetime
    window_end: datetime
    risk_level: str
    emotion_distribution: dict
    representative_quote: str | None = None


class SearchResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[SearchResultItem]

from __future__ import annotations

from pydantic import BaseModel, Field


class KeywordSuggestRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1, description="Input texts to extract event keywords from")
    max_keywords: int = Field(3, ge=1, le=5)


class KeywordSuggestResponse(BaseModel):
    keywords: list[str]

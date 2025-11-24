from __future__ import annotations

from datetime import datetime, timedelta

from pydantic import BaseModel, Field, validator


class EventRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=128)
    hours: int = Field(6, ge=1, le=72)


class EmotionPoint(BaseModel):
    timestamp: datetime
    positive: float
    neutral: float
    negative: float


class CrisisSummary(BaseModel):
    max_probability: float
    avg_probability: float
    high_risk_count: int


class RepresentativeQuote(BaseModel):
    text: str
    label: str
    crisis_probability: float
    timestamp: datetime


class EventInsight(BaseModel):
    keyword: str
    window_start: datetime
    window_end: datetime
    emotion_series: list[EmotionPoint]
    crisis_summary: CrisisSummary
    representative_quotes: list[RepresentativeQuote]
    network_graph: dict
    export_links: list[str] = Field(default_factory=list)

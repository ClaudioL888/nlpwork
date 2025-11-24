from __future__ import annotations

import hashlib
import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SentimentLabel(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class EvidenceChunk(BaseModel):
    text: str
    label: str
    weight: float


class SentimentResult(BaseModel):
    label: SentimentLabel
    confidence: float
    scores: dict[SentimentLabel, float]


class EmpathyResult(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    rationale: str


class CrisisResult(BaseModel):
    probability: float = Field(ge=0.0, le=1.0)
    indicators: list[str]


class AnalyzerResult(BaseModel):
    request_id: str
    text: str
    text_hash: str
    sentiment: SentimentResult
    empathy: EmpathyResult
    crisis: CrisisResult
    evidence: list[EvidenceChunk]
    model_version: str
    rule_version: str | None = None
    latency_ms: float


def hash_text(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def build_request_id(prefix: str = "req") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def normalize_scores(scores: dict[SentimentLabel, float]) -> dict[SentimentLabel, float]:
    total = sum(scores.values()) or 1.0
    return {label: value / total for label, value in scores.items()}


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


class RuleMatch(BaseModel):
    rule_id: str
    description: str
    action: str
    severity: str
    tags: list[str]
    evidence: list[str]
    metadata: dict[str, Any] = Field(default_factory=dict)

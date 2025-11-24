from __future__ import annotations

from pydantic import BaseModel, Field

from src.core.nlp.types import AnalyzerResult, SentimentLabel


class AnalyzeTextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2048)


class AnalyzeTextResponse(BaseModel):
    request_id: str
    text: str
    text_hash: str
    label: SentimentLabel
    confidence: float
    empathy_score: float
    crisis_probability: float
    evidence: list[dict]
    model_version: str
    rule_version: str | None = None
    latency_ms: float

    @classmethod
    def from_result(cls, result: AnalyzerResult) -> "AnalyzeTextResponse":
        return cls(
            request_id=result.request_id,
            text=result.text,
            text_hash=result.text_hash,
            label=result.sentiment.label,
            confidence=result.sentiment.confidence,
            empathy_score=result.empathy.score,
            crisis_probability=result.crisis.probability,
            evidence=[chunk.model_dump() for chunk in result.evidence],
            model_version=result.model_version,
            rule_version=result.rule_version,
            latency_ms=result.latency_ms,
        )

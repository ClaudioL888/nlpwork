from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from src.core.nlp.types import AnalyzerResult


class FilterDecision(str, Enum):
    allow = "allow"
    review = "review"
    block = "block"


class FilterRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2048)


class FilterEvidence(BaseModel):
    rule_id: str
    description: str
    action: str
    severity: str
    tags: list[str]
    evidence: list[str]


class FilterResponse(BaseModel):
    request_id: str
    text_hash: str
    decision: FilterDecision
    allow: bool
    labels: list[str]
    matched_rules: list[FilterEvidence]
    analyzer_snapshot: dict

    @classmethod
    def from_decision(
        cls,
        decision: FilterDecision,
        allow: bool,
        matched_rules: list[FilterEvidence],
        analyzer_result: AnalyzerResult,
    ) -> "FilterResponse":
        return cls(
            request_id=analyzer_result.request_id,
            text_hash=analyzer_result.text_hash,
            decision=decision,
            allow=allow,
            labels=[analyzer_result.sentiment.label.value],
            matched_rules=matched_rules,
            analyzer_snapshot={
                "label": analyzer_result.sentiment.label.value,
                "confidence": analyzer_result.sentiment.confidence,
                "empathy_score": analyzer_result.empathy.score,
                "crisis_probability": analyzer_result.crisis.probability,
                "model_version": analyzer_result.model_version,
                "rule_version": analyzer_result.rule_version,
            },
        )

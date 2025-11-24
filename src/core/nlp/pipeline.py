from __future__ import annotations

import math
import time
from typing import Any

from src.core.logging.config import get_logger
from src.core.nlp.llm_classifier import LLMClassifier
from src.core.nlp.model_registry import ModelRegistry, registry
from src.core.nlp.types import (
    AnalyzerResult,
    CrisisResult,
    EmpathyResult,
    EvidenceChunk,
    RuleMatch,
    SentimentLabel,
    SentimentResult,
    clamp,
    hash_text,
    build_request_id,
    normalize_scores,
)


class SentimentClassifier:
    def __init__(
        self,
        registry: ModelRegistry,
        model_name: str = "demo-sentiment",
        version: str = "1.0.0",
    ) -> None:
        default_manifest = {
            "name": model_name,
            "version": version,
            "labels": ["positive", "neutral", "negative"],
            "keywords": {
                "positive": ["great", "love", "awesome", "good", "开心", "感激"],
                "negative": ["hate", "angry", "terrible", "bad", "伤心", "愤怒"],
            },
        }
        self.manifest = registry.get_manifest(model_name, version, default_manifest)

    def predict(self, text: str) -> SentimentResult:
        text_lower = text.lower()
        scores = {
            SentimentLabel.positive: 0.1,
            SentimentLabel.neutral: 0.1,
            SentimentLabel.negative: 0.1,
        }
        for label_name, keywords in self.manifest.get("keywords", {}).items():
            label = SentimentLabel(label_name)
            for kw in keywords:
                if kw.lower() in text_lower:
                    scores[label] += 1.0
        if scores[SentimentLabel.positive] == scores[SentimentLabel.negative]:
            scores[SentimentLabel.neutral] += 0.5

        normalized = normalize_scores(scores)
        label = max(normalized, key=normalized.get)
        confidence = normalized[label]
        return SentimentResult(label=label, confidence=confidence, scores=normalized)


class EmpathyScorer:
    def __init__(
        self,
        registry: ModelRegistry,
        model_name: str = "demo-empathy",
        version: str = "1.0.0",
    ) -> None:
        default_manifest = {
            "keywords": ["sorry", "理解", "care", "support", "抱歉", "感谢", "empathy"]
        }
        self.manifest = registry.get_manifest(model_name, version, default_manifest)

    def score(self, text: str) -> EmpathyResult:
        matches = [
            kw for kw in self.manifest.get("keywords", []) if kw.lower() in text.lower()
        ]
        score = clamp(len(matches) / 3.0)
        rationale = (
            "Detected empathic cues: " + ", ".join(matches) if matches else "Neutral tone"
        )
        return EmpathyResult(score=score, rationale=rationale)


class CrisisDetector:
    def __init__(
        self,
        registry: ModelRegistry,
        model_name: str = "demo-crisis",
        version: str = "1.0.0",
    ) -> None:
        default_manifest = {
            "keywords": ["suicide", "kill myself", "暴力", "恐吓", "爆炸", "伤害"],
            "boost": ["now", "immediately", "立刻"],
        }
        self.manifest = registry.get_manifest(model_name, version, default_manifest)

    def predict(self, text: str) -> RuleMatch:
        text_lower = text.lower()
        indicators = [
            kw
            for kw in self.manifest.get("keywords", [])
            if kw.lower() in text_lower
        ]
        boost = any(term in text_lower for term in self.manifest.get("boost", []))
        probability = clamp(len(indicators) * (1.5 if boost else 1) / 3.0)
        return RuleMatch(
            rule_id="crisis_model",
            description="Keyword-based crisis detector",
            action="review" if probability > 0.3 else "allow",
            severity="high" if probability > 0.7 else "medium",
            tags=["crisis"],
            evidence=indicators,
            metadata={"probability": probability},
        )


class NLPPipeline:
    def __init__(self, model_registry: ModelRegistry | None = None) -> None:
        self.registry = model_registry or registry
        self.sentiment = SentimentClassifier(self.registry)
        self.empathy = EmpathyScorer(self.registry)
        self.crisis = CrisisDetector(self.registry)
        self.logger = get_logger(__name__)
        self.llm = LLMClassifier()

    def analyze(self, text: str) -> AnalyzerResult:
        start = time.perf_counter()
        llm_result = self.llm.classify(text)

        if llm_result:
            sentiment = SentimentResult(
                label=SentimentLabel(llm_result.label),
                confidence=1.0 - abs(0.5 - llm_result.crisis_probability),
                scores={
                    SentimentLabel.positive: 1.0 if llm_result.label == "positive" else 0.0,
                    SentimentLabel.neutral: 1.0 if llm_result.label == "neutral" else 0.0,
                    SentimentLabel.negative: 1.0 if llm_result.label == "negative" else 0.0,
                },
            )
            empathy = self.empathy.score(text)
            crisis = RuleMatch(
                rule_id="llm_crisis",
                description="LLM-evaluated crisis probability",
                action="review" if llm_result.crisis_probability > 0.3 else "allow",
                severity="high" if llm_result.crisis_probability > 0.7 else "medium",
                tags=["crisis", "llm"],
                evidence=[],
                metadata={"probability": llm_result.crisis_probability, "rationale": llm_result.rationale},
            )
        else:
            sentiment = self.sentiment.predict(text)
            empathy = self.empathy.score(text)
            crisis = self.crisis.predict(text)

        evidence = []
        positive_words = [
            w.lower()
            for w in self.sentiment.manifest.get("keywords", {}).get("positive", [])
        ]
        negative_words = [
            w.lower()
            for w in self.sentiment.manifest.get("keywords", {}).get("negative", [])
        ]
        crisis_words = [w.lower() for w in self.crisis.manifest.get("keywords", [])]

        for token in text.split():
            lower = token.lower()
            if lower in positive_words + negative_words:
                evidence.append(EvidenceChunk(text=token, label="sentiment", weight=0.5))
            if lower in crisis_words:
                evidence.append(EvidenceChunk(text=token, label="crisis", weight=1.0))

        request_id = build_request_id()
        text_hash = hash_text(text)
        latency_ms = (time.perf_counter() - start) * 1000

        result = AnalyzerResult(
            request_id=request_id,
            text=text,
            text_hash=text_hash,
            sentiment=sentiment,
            empathy=empathy,
            crisis=crisis_to_result(crisis),
            evidence=evidence,
            model_version=self.sentiment.manifest.get("version", "1.0.0"),
            latency_ms=round(latency_ms, 2),
        )
        self.logger.debug(
            "nlp_pipeline.analyze",
            request_id=request_id,
            label=sentiment.label,
            empathy=empathy.score,
            crisis_prob=result.crisis.probability,
            latency_ms=result.latency_ms,
            llm_used=bool(llm_result),
        )
        return result


def crisis_to_result(match: RuleMatch) -> CrisisResult:
    probability = float(match.metadata.get("probability", 0.0))
    return CrisisResult(
        probability=clamp(probability),
        indicators=match.evidence,
    )

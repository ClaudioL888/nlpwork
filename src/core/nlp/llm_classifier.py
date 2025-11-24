from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal

import httpx

from src.config.settings import get_settings
from src.core.logging.config import get_logger


@dataclass
class LLMClassificationResult:
    label: Literal["positive", "neutral", "negative"]
    crisis_probability: float
    rationale: str | None = None


class LLMClassifier:
    """LLM-backed sentiment + crisis scorer. Falls back silently on errors."""

    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.llm.base_url
        self.api_key = settings.llm.api_key
        self.model = settings.llm.model
        self.enabled = settings.llm.enabled and bool(self.base_url and self.api_key)
        self.timeout = settings.llm.timeout_seconds
        self.logger = get_logger(__name__)

    def classify(self, text: str) -> LLMClassificationResult | None:
        if not self.enabled:
            return None

        prompt = (
            "You are a sentiment and crisis risk classifier. "
            "Given a message, respond with a strict JSON object containing: "
            '{"label": "positive|neutral|negative", '
            '"crisis_probability": float between 0 and 1, '
            '"rationale": "short reason"}'
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            "stream": False,
            "response_format": {"type": "json_object"},
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                resp = client.post("/chat/completions", json=payload, headers=headers)
                resp.raise_for_status()
                content = resp.json()
        except Exception as exc:  # pragma: no cover - external I/O
            self.logger.warning("llm.classify.failed", error=str(exc))
            return None

        try:
            message_content = content["choices"][0]["message"]["content"]
            data = message_content
            if isinstance(message_content, str):
                data = json.loads(message_content)
            label = data.get("label", "neutral")
            crisis_prob = float(data.get("crisis_probability", 0.0))
            rationale = data.get("rationale")
            if label not in {"positive", "neutral", "negative"}:
                label = "neutral"
            crisis_prob = max(0.0, min(1.0, crisis_prob))
            return LLMClassificationResult(
                label=label, crisis_probability=crisis_prob, rationale=rationale
            )
        except Exception as exc:  # pragma: no cover - parsing guard
            self.logger.warning("llm.classify.parse_error", error=str(exc))
            return None

from __future__ import annotations

import json
import re
from typing import List

import httpx

from src.config.settings import get_settings
from src.core.logging.config import get_logger


class KeywordSuggester:
    """Suggests event keywords from text using LLM when available, with heuristic fallback."""

    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.llm.base_url
        self.api_key = settings.llm.api_key
        self.model = settings.llm.model
        self.enabled = settings.llm.enabled and bool(self.base_url and self.api_key)
        self.timeout = settings.llm.timeout_seconds
        self.logger = get_logger(__name__)

    def suggest(self, text: str, max_keywords: int = 3) -> list[str]:
        if self.enabled:
            try:
                result = self._suggest_with_llm(text, max_keywords)
                if result:
                    return result
            except Exception as exc:  # pragma: no cover - network
                self.logger.warning("keyword_suggester.llm_failed", error=str(exc))
        return self._fallback(text, max_keywords)

    def _suggest_with_llm(self, text: str, max_keywords: int) -> list[str]:
        prompt = (
            "Extract concise event keywords (1-3 words each) from the USER content. "
            f"Return up to {max_keywords} keywords that best summarize the main event/topic. "
            "Respond strictly as JSON: {\"keywords\": [\"...\"]}"
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
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
            resp = client.post("/chat/completions", json=payload, headers=headers)
            resp.raise_for_status()
            content = resp.json()
        message_content = content["choices"][0]["message"]["content"]
        data = json.loads(message_content) if isinstance(message_content, str) else message_content
        keywords = data.get("keywords") or []
        cleaned = [kw.strip() for kw in keywords if isinstance(kw, str) and kw.strip()]
        return cleaned[:max_keywords]

    @staticmethod
    def _fallback(text: str, max_keywords: int) -> list[str]:
        tokens = re.findall(r"[A-Za-z]{4,}", text.lower())
        seen = set()
        keywords: List[str] = []
        for token in tokens:
            if token in seen:
                continue
            seen.add(token)
            keywords.append(token)
            if len(keywords) >= max_keywords:
                break
        return keywords or ["general"]


def get_keyword_suggester() -> KeywordSuggester:
    return KeywordSuggester()

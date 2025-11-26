from __future__ import annotations

from src.core.nlp.keyword_suggester import KeywordSuggester, get_keyword_suggester


class KeywordSuggestService:
    def __init__(self, suggester: KeywordSuggester) -> None:
        self.suggester = suggester

    def suggest_keywords(self, texts: list[str], max_keywords: int = 3) -> list[str]:
        keywords: list[str] = []
        for text in texts:
            keywords.extend(self.suggester.suggest(text, max_keywords))
        # de-duplicate while preserving order
        seen = set()
        deduped = []
        for kw in keywords:
            if kw in seen:
                continue
            seen.add(kw)
            deduped.append(kw)
        return deduped[:max_keywords]


def get_keyword_suggest_service() -> KeywordSuggestService:
    suggester = get_keyword_suggester()
    return KeywordSuggestService(suggester)

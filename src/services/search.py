from __future__ import annotations

from fastapi import Depends

from src.data.search_repo import SearchRepository
from src.db.session import get_session
from src.schemas.search import SearchRequest, SearchResponse, SearchResultItem


class SearchService:
    def __init__(self, repo: SearchRepository) -> None:
        self.repo = repo

    async def search(self, payload: SearchRequest) -> SearchResponse:
        offset = (payload.page - 1) * payload.page_size
        snapshots = await self.repo.search(payload.keyword, payload.page_size, offset)
        items = []
        for snapshot in snapshots:
            crisis_summary = snapshot.crisis_summary
            risk_level = "high" if crisis_summary.get("max_probability", 0) >= 0.7 else "medium"
            representative = None
            quotes = snapshot.representative_quotes
            if quotes:
                representative = quotes[0].get("text")
            items.append(
                SearchResultItem(
                    keyword=snapshot.keyword,
                    window_start=snapshot.window_start,
                    window_end=snapshot.window_end,
                    risk_level=risk_level,
                    emotion_distribution={
                        "positive": snapshot.emotion_series[0].get("positive", 0)
                        if snapshot.emotion_series
                        else 0,
                        "neutral": snapshot.emotion_series[0].get("neutral", 0)
                        if snapshot.emotion_series
                        else 0,
                        "negative": snapshot.emotion_series[0].get("negative", 0)
                        if snapshot.emotion_series
                        else 0,
                    },
                    representative_quote=representative,
                )
            )
        total = await self.repo.count(payload.keyword)
        return SearchResponse(total=total, page=payload.page, page_size=payload.page_size, results=items)


async def get_search_service(
    session=Depends(get_session),
) -> SearchService:
    repo = SearchRepository(session)
    return SearchService(repo)

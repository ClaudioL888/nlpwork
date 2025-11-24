from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.event_snapshot import EventSnapshot


class EventSnapshotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_latest(self, keyword: str) -> EventSnapshot | None:
        stmt = (
            select(EventSnapshot)
            .where(EventSnapshot.keyword == keyword)
            .order_by(EventSnapshot.window_end.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def save_snapshot(
        self,
        keyword: str,
        window_start: datetime,
        window_end: datetime,
        emotion_series: list[dict],
        crisis_summary: dict,
        representative_quotes: list[dict],
        network_graph: dict,
    ) -> EventSnapshot:
        snapshot = EventSnapshot(
            keyword=keyword,
            window_start=window_start,
            window_end=window_end,
            emotion_series=emotion_series,
            crisis_summary=crisis_summary,
            representative_quotes=representative_quotes,
            network_graph=network_graph,
        )
        self.session.add(snapshot)
        await self.session.flush()
        await self.session.commit()
        return snapshot

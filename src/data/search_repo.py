from __future__ import annotations

from sqlalchemy import select, or_, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.event_snapshot import EventSnapshot


class SearchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _keyword_filter(self, keyword: str):
        pattern = f"%{keyword}%"
        return or_(
            EventSnapshot.keyword.ilike(pattern),
            cast(EventSnapshot.representative_quotes, String).ilike(pattern),
        )

    async def search(self, keyword: str, limit: int, offset: int) -> list[EventSnapshot]:
        stmt = (
            select(EventSnapshot)
            .where(self._keyword_filter(keyword))
            .order_by(EventSnapshot.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count(self, keyword: str) -> int:
        stmt = select(EventSnapshot).where(self._keyword_filter(keyword))
        result = await self.session.execute(stmt)
        return len(result.scalars().all())

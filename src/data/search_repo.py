from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.event_snapshot import EventSnapshot


class SearchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def search(self, keyword: str, limit: int, offset: int) -> list[EventSnapshot]:
        stmt = (
            select(EventSnapshot)
            .where(EventSnapshot.keyword.ilike(f"%{keyword}%"))
            .order_by(EventSnapshot.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count(self, keyword: str) -> int:
        stmt = select(EventSnapshot).where(EventSnapshot.keyword.ilike(f"%{keyword}%"))
        result = await self.session.execute(stmt)
        return len(result.scalars().all())

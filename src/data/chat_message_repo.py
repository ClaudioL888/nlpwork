from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.chat_message import ChatMessage


class ChatMessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_message(self, message: ChatMessage) -> ChatMessage:
        self.session.add(message)
        await self.session.flush()
        await self.session.commit()
        return message

    async def recent_messages(self, room_id: str, limit: int = 20) -> list[ChatMessage]:
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.room_id == room_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(reversed(result.scalars().all()))

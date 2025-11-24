from __future__ import annotations

import asyncio
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect

from src.core.rate_limit import InMemoryRateLimiter
from src.data.chat_message_repo import ChatMessageRepository
from src.models.chat_message import ChatMessage
from src.schemas.chat import ChatMessagePayload, ChatMessageResponse
from src.services.analyzer import AnalyzerService, get_analyzer_service


class ChatGateway:
    def __init__(
        self,
        analyzer: AnalyzerService,
        repo: ChatMessageRepository,
        rate_limiter: InMemoryRateLimiter | None = None,
    ) -> None:
        self.analyzer = analyzer
        self.repo = repo
        self.rate_limiter = rate_limiter or InMemoryRateLimiter(max_events=5, per_seconds=1)
        self.connections: dict[str, set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str) -> None:
        await websocket.accept()
        self.connections.setdefault(room_id, set()).add(websocket)
        history = await self.repo.recent_messages(room_id)
        for message in history:
            await websocket.send_json(self._serialize_message(message))

    def disconnect(self, websocket: WebSocket, room_id: str) -> None:
        self.connections.get(room_id, set()).discard(websocket)

    async def handle_message(self, websocket: WebSocket, payload: ChatMessagePayload) -> None:
        if not self.rate_limiter.check(payload.user_id):
            await websocket.send_json({"type": "error", "code": "RATE_LIMIT"})
            return
        result = await self.analyzer.analyze_text(payload.text)
        message = ChatMessage(
            room_id=payload.room_id,
            user_id=payload.user_id,
            text=payload.text,
            sentiment=result.sentiment.label.value,
            crisis_probability=result.crisis.probability,
        )
        await self.repo.add_message(message)
        await self.broadcast(payload.room_id, self._serialize_message(message))

    async def broadcast(self, room_id: str, message: dict[str, Any]) -> None:
        room_connections = self.connections.get(room_id, set())
        await asyncio.gather(*(conn.send_json(message) for conn in room_connections))

    @staticmethod
    def _serialize_message(message: ChatMessage) -> dict[str, Any]:
        payload = ChatMessageResponse(
            room_id=message.room_id,
            user_id=message.user_id,
            text=message.text,
            sentiment=message.sentiment,
            crisis_probability=message.crisis_probability,
            created_at=message.created_at,
        ).model_dump()
        payload["created_at"] = message.created_at.isoformat()
        return payload

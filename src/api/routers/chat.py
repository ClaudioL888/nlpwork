from __future__ import annotations

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from src.data.chat_message_repo import ChatMessageRepository
from src.db.session import get_session
from src.schemas.chat import ChatMessagePayload
from src.services.analyzer import AnalyzerService, get_analyzer_service
from src.services.chat_gateway import ChatGateway

router = APIRouter()


async def get_gateway(
    analyzer: AnalyzerService = Depends(get_analyzer_service),
    session=Depends(get_session),
) -> ChatGateway:
    repo = ChatMessageRepository(session)
    return ChatGateway(analyzer=analyzer, repo=repo)


@router.websocket("/ws/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    user_id: str,
    gateway: ChatGateway = Depends(get_gateway),
) -> None:
    await gateway.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_json()
            payload = ChatMessagePayload(room_id=room_id, user_id=user_id, text=data.get("text", ""))
            await gateway.handle_message(websocket, payload)
    except WebSocketDisconnect:
        gateway.disconnect(websocket, room_id)

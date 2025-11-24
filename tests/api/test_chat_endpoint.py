import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.api.routers.chat import get_gateway
from src.schemas.chat import ChatMessagePayload


class DummyGateway:
    async def connect(self, websocket, room_id):
        await websocket.accept()

    def disconnect(self, websocket, room_id):
        return None

    async def handle_message(self, websocket, payload: ChatMessagePayload):
        await websocket.send_json(
            {
                "room_id": payload.room_id,
                "user_id": payload.user_id,
                "text": payload.text,
                "sentiment": "neutral",
                "crisis_probability": 0.1,
                "created_at": "2025-11-14T00:00:00Z",
            }
        )


def override_gateway():
    return DummyGateway()


def test_chat_websocket(monkeypatch):
    app.dependency_overrides[get_gateway] = override_gateway
    client = TestClient(app)
    with client.websocket_connect("/ws/chat?room_id=room1&user_id=demo") as websocket:
        websocket.send_json({"text": "hello"})
        message = websocket.receive_json()
        assert message["text"] == "hello"
    app.dependency_overrides.clear()

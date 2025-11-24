from starlette.testclient import TestClient

from src.app import app


def test_chat_websocket_flow():
    client = TestClient(app)
    with client.websocket_connect("/ws/chat?room_id=test&user_id=integration") as websocket:
        websocket.send_json({"text": "hello world"})
        message = websocket.receive_json()
        assert message["text"] == "hello world"
        assert message["sentiment"].lower() in {"positive", "neutral", "negative"}

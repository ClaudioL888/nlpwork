from fastapi.testclient import TestClient

from src.app import app
from src.config.settings import get_settings
from src.services.analyzer import AnalyzerService, get_analyzer_service


def override_service() -> AnalyzerService:
    return AnalyzerService()


def test_analyze_text_endpoint(monkeypatch):
    app.dependency_overrides[get_analyzer_service] = override_service
    client = TestClient(app)
    client.headers.update({"x-api-key": get_settings().security.api_key})

    response = client.post("/api/analyze_text", json={"text": "I love this"})

    assert response.status_code == 200
    body = response.json()
    assert body["label"] in {"positive", "neutral", "negative"}
    assert body["request_id"]
    app.dependency_overrides.clear()


def test_analyze_text_empty(monkeypatch):
    app.dependency_overrides[get_analyzer_service] = override_service
    client = TestClient(app)
    client.headers.update({"x-api-key": get_settings().security.api_key})

    response = client.post("/api/analyze_text", json={"text": "   "})
    assert response.status_code == 422
    app.dependency_overrides.clear()

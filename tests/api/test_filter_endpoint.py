from fastapi.testclient import TestClient

from src.app import app
from src.config.settings import get_settings
from src.services.analyzer import AnalyzerService, get_analyzer_service
from src.services.filter import FilterService, get_filter_service


def override_filter_service() -> FilterService:
    analyzer = AnalyzerService()
    return FilterService(analyzer=analyzer, audit_repo=None)  # type: ignore[arg-type]


def test_filter_endpoint(monkeypatch):
    app.dependency_overrides[get_filter_service] = override_filter_service
    client = TestClient(app)
    client.headers.update({"x-api-key": get_settings().security.api_key})

    response = client.post("/api/filter", json={"text": "I feel like suicide now"})

    assert response.status_code == 200
    body = response.json()
    assert body["decision"] in {"allow", "review", "block"}
    assert body["request_id"]
    app.dependency_overrides.clear()


def test_filter_empty(monkeypatch):
    app.dependency_overrides[get_filter_service] = override_filter_service
    client = TestClient(app)
    client.headers.update({"x-api-key": get_settings().security.api_key})

    response = client.post("/api/filter", json={"text": "   "})
    assert response.status_code == 422
    app.dependency_overrides.clear()

from fastapi.testclient import TestClient

from src.app import app
from src.config.settings import get_settings
from src.schemas.search import SearchResponse
from src.services.search import SearchService, get_search_service


class DummySearchService:
    async def search(self, payload):
        return SearchResponse(total=1, page=1, page_size=10, results=[])


def override_service() -> SearchService:
    return DummySearchService()  # type: ignore[return-value]


def test_search_endpoint(monkeypatch):
    app.dependency_overrides[get_search_service] = override_service
    client = TestClient(app)
    client.headers.update({"x-api-key": get_settings().security.api_key})
    response = client.post("/api/search", json={"keyword": "earthquake"})
    assert response.status_code == 200
    app.dependency_overrides.clear()


def test_search_validation(monkeypatch):
    app.dependency_overrides[get_search_service] = override_service
    client = TestClient(app)
    client.headers.update({"x-api-key": get_settings().security.api_key})
    response = client.post("/api/search", json={"keyword": "   "})
    assert response.status_code == 422
    app.dependency_overrides.clear()

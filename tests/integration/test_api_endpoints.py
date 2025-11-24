import httpx
import pytest
import pytest_asyncio
from httpx import ASGITransport

from src.app import app
from src.config.settings import get_settings


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        client.headers["x-api-key"] = get_settings().security.api_key
        yield client


@pytest.mark.asyncio
async def test_health(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_analyze_text_flow(async_client):
    response = await async_client.post("/api/analyze_text", json={"text": "I love this system"})
    body = response.json()
    assert response.status_code == 200
    assert body["label"] in {"positive", "neutral", "negative"}


@pytest.mark.asyncio
async def test_filter_flow(async_client):
    response = await async_client.post("/api/filter", json={"text": "I hate you"})
    assert response.status_code == 200
    assert "decision" in response.json()


@pytest.mark.asyncio
async def test_metrics_exposed(async_client):
    response = await async_client.get("/metrics", follow_redirects=True)
    assert response.status_code == 200
    assert b"dep_requests_total" in response.content

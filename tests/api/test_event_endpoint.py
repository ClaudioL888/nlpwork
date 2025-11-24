from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from src.app import app
from src.config.settings import get_settings
from src.schemas.event import EventInsight, EmotionPoint, CrisisSummary, RepresentativeQuote
from src.services.event_analyzer import EventAnalyzerService, get_event_analyzer_service


class DummyEventAnalyzer:
    async def analyze_event(self, keyword: str, hours: int) -> EventInsight:
        now = datetime.utcnow()
        return EventInsight(
            keyword=keyword,
            window_start=now - timedelta(hours=hours),
            window_end=now,
            emotion_series=[
                EmotionPoint(timestamp=now, positive=0.5, neutral=0.3, negative=0.2)
            ],
            crisis_summary=CrisisSummary(max_probability=0.8, avg_probability=0.4, high_risk_count=1),
            representative_quotes=[
                RepresentativeQuote(
                    text="sample", label="positive", crisis_probability=0.2, timestamp=now
                )
            ],
            network_graph={"nodes": [], "edges": []},
        )


def override_event_service() -> EventAnalyzerService:
    return DummyEventAnalyzer()  # type: ignore[return-value]


def test_analyze_event_endpoint(monkeypatch):
    app.dependency_overrides[get_event_analyzer_service] = override_event_service
    client = TestClient(app)
    client.headers.update({"x-api-key": get_settings().security.api_key})

    response = client.post("/api/analyze_event", json={"keyword": "earthquake", "hours": 4})
    assert response.status_code == 200
    body = response.json()
    assert body["keyword"] == "earthquake"
    app.dependency_overrides.clear()


def test_analyze_event_validation(monkeypatch):
    app.dependency_overrides[get_event_analyzer_service] = override_event_service
    client = TestClient(app)
    client.headers.update({"x-api-key": get_settings().security.api_key})
    response = client.post("/api/analyze_event", json={"keyword": "  ", "hours": 4})
    assert response.status_code == 422
    app.dependency_overrides.clear()

from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.db.base import Base
from src.services.search import SearchService
from src.data.search_repo import SearchRepository
from src.models.event_snapshot import EventSnapshot
from src.schemas.search import SearchRequest


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_search_service_returns_results(session):
    snapshot = EventSnapshot(
        keyword="earthquake",
        window_start=datetime.utcnow(),
        window_end=datetime.utcnow(),
        emotion_series=[{"positive": 0.2, "neutral": 0.5, "negative": 0.3, "timestamp": datetime.utcnow().isoformat()}],
        crisis_summary={"max_probability": 0.8},
        representative_quotes=[{"text": "sample"}],
        network_graph={"nodes": [], "edges": []},
    )
    session.add(snapshot)
    await session.commit()

    repo = SearchRepository(session)
    service = SearchService(repo)
    response = await service.search(SearchRequest(keyword="earthquake", page=1, page_size=5, sort="risk"))
    assert response.total == 1
    assert response.results[0].keyword == "earthquake"

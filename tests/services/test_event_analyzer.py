from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.db.base import Base
from src.services.analyzer import AnalyzerService
from src.services.event_analyzer import EventAnalyzerService
from src.data.analysis_log_repo import AnalysisLogRepository
from src.models.analysis_log import AnalysisLog


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
async def test_event_analyzer_builds_series(session):
    repo = AnalysisLogRepository(session)
    analyzer = AnalyzerService(repo=repo)
    await analyzer.analyze_text("earthquake keyword positive news")
    await analyzer.analyze_text("earthquake keyword negative news")

    result = await session.execute(select(AnalysisLog))
    logs = result.scalars().all()
    now = datetime.utcnow()
    for idx, log in enumerate(logs):
        log.created_at = now - timedelta(hours=idx)
    await session.commit()

    service = EventAnalyzerService(session)
    insight = await service.analyze_event("earthquake", hours=6)

    assert insight.keyword == "earthquake"
    assert insight.emotion_series
    assert insight.representative_quotes
    assert insight.network_graph["nodes"]

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.nlp.types import SentimentLabel
from src.db.base import Base
from src.services.analyzer import AnalyzerService
from src.data.analysis_log_repo import AnalysisLogRepository


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
async def test_analyzer_service_logs_results(session):
    repo = AnalysisLogRepository(session)
    service = AnalyzerService(repo=repo)

    result = await service.analyze_text("I love this amazing tool")

    assert result.sentiment.label == SentimentLabel.positive
    stored = await repo.get_by_request_id(result.request_id)
    assert stored is not None
    assert stored.label == SentimentLabel.positive.value

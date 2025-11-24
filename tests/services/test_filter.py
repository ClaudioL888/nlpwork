import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.nlp.types import SentimentLabel
from src.db.base import Base
from src.services.filter import FilterService
from src.schemas.filter import FilterDecision
from src.services.analyzer import AnalyzerService
from src.data.filter_audit_repo import FilterAuditRepository
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
async def test_filter_service_flags_matches(session):
    analyzer_repo = AnalysisLogRepository(session)
    analyzer_service = AnalyzerService(repo=analyzer_repo)
    audit_repo = FilterAuditRepository(session)
    service = FilterService(analyzer=analyzer_service, audit_repo=audit_repo)

    decision, allow, matches, analyzer_result = await service.filter_text(
        "I hate you, you are a 废物"
    )

    assert decision == FilterDecision.review
    assert not allow
    assert matches
    stored = await audit_repo.get_by_request_id(analyzer_result.request_id)
    assert stored is not None
    assert stored.allow is False

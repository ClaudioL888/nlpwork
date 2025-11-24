from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.nlp.types import AnalyzerResult
from src.models.analysis_log import AnalysisLog


class AnalysisLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_from_result(self, result: AnalyzerResult) -> AnalysisLog:
        log = AnalysisLog(
            request_id=result.request_id,
            text_hash=result.text_hash,
            text=result.text,
            label=result.sentiment.label.value,
            empathy_score=result.empathy.score,
            crisis_probability=result.crisis.probability,
            evidence=[chunk.model_dump() for chunk in result.evidence],
            model_version=result.model_version,
            rule_version=result.rule_version,
        )
        self.session.add(log)
        await self.session.flush()
        await self.session.commit()
        return log

    async def get_by_request_id(self, request_id: str) -> AnalysisLog | None:
        result = await self.session.execute(
            select(AnalysisLog).where(AnalysisLog.request_id == request_id)
        )
        return result.scalar_one_or_none()

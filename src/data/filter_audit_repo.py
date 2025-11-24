from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.nlp.types import AnalyzerResult
from src.models.filter_audit import FilterAudit


class FilterAuditRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        request_id: str,
        text_hash: str,
        decision: str,
        reason: str,
        allow: bool,
        matched_rules: list[dict],
        analyzer_result: AnalyzerResult,
    ) -> FilterAudit:
        audit = FilterAudit(
            request_id=request_id,
            text_hash=text_hash,
            decision=decision,
            reason=reason,
            allow=allow,
            matched_rules=matched_rules,
            analyzer_snapshot={
                "label": analyzer_result.sentiment.label.value,
                "confidence": analyzer_result.sentiment.confidence,
                "empathy_score": analyzer_result.empathy.score,
                "crisis_probability": analyzer_result.crisis.probability,
                "model_version": analyzer_result.model_version,
                "rule_version": analyzer_result.rule_version,
            },
        )
        self.session.add(audit)
        await self.session.flush()
        await self.session.commit()
        return audit

    async def get_by_request_id(self, request_id: str) -> FilterAudit | None:
        result = await self.session.execute(
            select(FilterAudit).where(FilterAudit.request_id == request_id)
        )
        return result.scalar_one_or_none()

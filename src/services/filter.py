from __future__ import annotations

from fastapi import Depends

from src.core.nlp.rule_matcher import RuleMatcher
from src.core.nlp.types import AnalyzerResult
from src.data.analysis_log_repo import AnalysisLogRepository
from src.data.filter_audit_repo import FilterAuditRepository
from src.db.session import get_session
from src.schemas.filter import FilterDecision
from src.services.analyzer import AnalyzerService, get_analyzer_service


class FilterService:
    def __init__(
        self,
        analyzer: AnalyzerService,
        audit_repo: FilterAuditRepository | None = None,
        rule_matcher: RuleMatcher | None = None,
    ) -> None:
        self.analyzer = analyzer
        self.audit_repo = audit_repo
        self.rule_matcher = rule_matcher or RuleMatcher()

    async def filter_text(self, text: str) -> tuple[FilterDecision, bool, list, AnalyzerResult]:
        analyzer_result = await self.analyzer.analyze_text(text)
        matches = self.rule_matcher.match(text)
        crisis_prob = analyzer_result.crisis.probability

        if matches:
            decision = FilterDecision.review
            allow = False
            reason = "Matched content rules"
        elif crisis_prob > 0.7:
            decision = FilterDecision.block
            allow = False
            reason = "High crisis probability"
        else:
            decision = FilterDecision.allow
            allow = True
            reason = "Clean"

        if self.audit_repo is not None:
            await self.audit_repo.create(
                request_id=analyzer_result.request_id,
                text_hash=analyzer_result.text_hash,
                decision=decision.value,
                reason=reason,
                allow=allow,
                matched_rules=[match.model_dump() for match in matches],
                analyzer_result=analyzer_result,
            )
        return decision, allow, matches, analyzer_result


async def get_filter_service(
    analyzer: AnalyzerService = Depends(get_analyzer_service),
    session=Depends(get_session),
) -> FilterService:
    audit_repo = FilterAuditRepository(session)
    return FilterService(analyzer=analyzer, audit_repo=audit_repo)

from __future__ import annotations

from fastapi import Depends

from src.core.nlp.pipeline import NLPPipeline
from src.core.nlp.types import AnalyzerResult
from src.data.analysis_log_repo import AnalysisLogRepository
from src.db.session import get_session


class AnalyzerService:
    def __init__(
        self,
        pipeline: NLPPipeline | None = None,
        repo: AnalysisLogRepository | None = None,
    ) -> None:
        self.pipeline = pipeline or NLPPipeline()
        self.repo = repo

    async def analyze_text(self, text: str) -> AnalyzerResult:
        result = self.pipeline.analyze(text)
        if self.repo is not None:
            await self.repo.create_from_result(result)
        return result


async def get_analyzer_service(
    session=Depends(get_session),
) -> AnalyzerService:
    repo = AnalysisLogRepository(session)
    return AnalyzerService(repo=repo)

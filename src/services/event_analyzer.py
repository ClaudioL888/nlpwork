from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.graph.builder import build_sentiment_graph
from src.db.session import get_session
from src.models.analysis_log import AnalysisLog
from src.data.event_snapshot_repo import EventSnapshotRepository
from src.schemas.event import EventInsight, EmotionPoint, CrisisSummary, RepresentativeQuote


class EventAnalyzerService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.snapshot_repo = EventSnapshotRepository(session)

    async def analyze_event(self, keyword: str, hours: int) -> EventInsight:
        window_end = datetime.utcnow()
        window_start = window_end - timedelta(hours=hours)
        stmt = select(AnalysisLog).where(AnalysisLog.created_at >= window_start)
        if keyword:
            stmt = stmt.where(AnalysisLog.text.ilike(f"%{keyword}%"))
        stmt = stmt.order_by(AnalysisLog.created_at)
        result = await self.session.execute(stmt)
        logs = result.scalars().all()

        if not logs:
            snapshot = await self.snapshot_repo.get_latest(keyword)
            if snapshot:
                return EventInsight(
                    keyword=keyword,
                    window_start=snapshot.window_start,
                    window_end=snapshot.window_end,
                    emotion_series=[EmotionPoint(**point) for point in snapshot.emotion_series],
                    crisis_summary=CrisisSummary(**snapshot.crisis_summary),
                    representative_quotes=[RepresentativeQuote(**quote) for quote in snapshot.representative_quotes],
                    network_graph=snapshot.network_graph,
                )
            return EventInsight(
                keyword=keyword,
                window_start=window_start,
                window_end=window_end,
                emotion_series=[],
                crisis_summary=CrisisSummary(max_probability=0.0, avg_probability=0.0, high_risk_count=0),
                representative_quotes=[],
                network_graph={"nodes": [], "edges": []},
            )

        emotion_series = build_emotion_series(logs, window_start, window_end)
        crisis_summary = build_crisis_summary(logs)
        quotes = build_representative_quotes(logs)
        graph = build_sentiment_graph([quote.model_dump() for quote in quotes])

        await self.snapshot_repo.save_snapshot(
            keyword=keyword,
            window_start=window_start,
            window_end=window_end,
            emotion_series=[
                {**point.model_dump(), "timestamp": point.timestamp.isoformat()}
                for point in emotion_series
            ],
            crisis_summary=crisis_summary.model_dump(),
            representative_quotes=[
                {**quote.model_dump(), "timestamp": quote.timestamp.isoformat()}
                for quote in quotes
            ],
            network_graph=graph,
        )

        return EventInsight(
            keyword=keyword,
            window_start=window_start,
            window_end=window_end,
            emotion_series=emotion_series,
            crisis_summary=crisis_summary,
            representative_quotes=quotes,
            network_graph=graph,
        )


def build_emotion_series(logs, window_start: datetime, window_end: datetime) -> list[EmotionPoint]:
    buckets: dict[datetime, dict[str, int]] = {}
    for log in logs:
        bucket_time = log.created_at.replace(minute=0, second=0, microsecond=0)
        bucket = buckets.setdefault(bucket_time, {"positive": 0, "neutral": 0, "negative": 0})
        bucket[log.label] = bucket.get(log.label, 0) + 1
    points = []
    for timestamp in sorted(buckets):
        bucket = buckets[timestamp]
        total = sum(bucket.values()) or 1
        points.append(
            EmotionPoint(
                timestamp=timestamp,
                positive=bucket.get("positive", 0) / total,
                neutral=bucket.get("neutral", 0) / total,
                negative=bucket.get("negative", 0) / total,
            )
        )
    if not points:
        points.append(
            EmotionPoint(timestamp=window_start, positive=0, neutral=1, negative=0)
        )
    return points


def build_crisis_summary(logs) -> CrisisSummary:
    probs = [log.crisis_probability for log in logs]
    max_prob = max(probs)
    avg_prob = sum(probs) / len(probs)
    high_risk = len([p for p in probs if p >= 0.7])
    return CrisisSummary(max_probability=max_prob, avg_probability=avg_prob, high_risk_count=high_risk)


def build_representative_quotes(logs) -> list[RepresentativeQuote]:
    sorted_logs = sorted(logs, key=lambda log: log.crisis_probability, reverse=True)
    quotes = []
    for log in sorted_logs[:5]:
        quotes.append(
            RepresentativeQuote(
                text=log.text,
                label=log.label,
                crisis_probability=log.crisis_probability,
                timestamp=log.created_at,
            )
        )
    return quotes


async def get_event_analyzer_service(
    session: AsyncSession = Depends(get_session),
) -> EventAnalyzerService:
    return EventAnalyzerService(session)

from __future__ import annotations

import asyncio
import random
from typing import Iterable
from datetime import datetime, timedelta

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config.settings import get_settings
from src.data.analysis_log_repo import AnalysisLogRepository
from src.data.chat_message_repo import ChatMessageRepository
from src.models.chat_message import ChatMessage
from src.models.analysis_log import AnalysisLog
from src.services.analyzer import AnalyzerService
from src.services.event_analyzer import EventAnalyzerService
from src.core.nlp.keyword_suggester import KeywordSuggester


def _random_users(n: int) -> Iterable[str]:
    for idx in range(n):
        yield f"user-seed{idx+1}"


async def analyze_with_llm(analyzer: AnalyzerService, content: str):
    attempts = 0
    last_result = None
    while attempts < 3:
        result = await analyzer.analyze_text(content)
        last_result = result
        if result.llm_used:
            return result
        attempts += 1
        await asyncio.sleep(0.5)
    raise RuntimeError(
        f"LLM was not used for content after retries: {content!r}. Last result llm_used={last_result.llm_used}"
    )


async def main() -> None:
    settings = get_settings()
    engine = create_async_engine(settings.database.url, future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    # wipe existing data
    async with engine.begin() as conn:
        for table in ("chat_messages", "filter_audits", "event_snapshots", "analysis_logs"):
            await conn.execute(text(f"DELETE FROM {table}"))

    async with async_session() as session:
        analyzer_repo = AnalysisLogRepository(session)
        analyzer = AnalyzerService(repo=analyzer_repo)
        keyword_suggester = KeywordSuggester()

        # seed analysis logs with mixed sentiments/crisis cases (all via LLM)
        seed_texts = [
            # earthquake-heavy to enrich charts
            "earthquake panic is rising downtown and people need help",
            "earthquake relief teams are doing an amazing job with aftershock risks",
            "earthquake aftershocks kept us awake all night, feeling scared",
            "major earthquake destroyed several bridges, responders are overwhelmed",
            "earthquake shelters are crowded but volunteers keep spirits high",
            "earthquake donations arrived early, giving hope to families",
            "earthquake rumors are causing panic on social media",
            "earthquake recovery is slow, I hate waiting with no water",
            "earthquake medical tents are low on supplies, people feel abandoned",
            "earthquake engineers say aftershocks may continue today",
            "earthquake counseling hotline is busy, I feel hopeless",
            "earthquake victims show resilience, rebuilding together",
            "earthquake power outage makes everyone nervous tonight",
            "earthquake emergency drills helped but fear remains",
            "earthquake heroes rescued children from collapsed school",
            "earthquake misinformation is spreading violence threats online",
            # other crises
            "wildfire smoke is choking the city, please send masks",
            "community volunteers bring hope after the wildfire evacuation",
            "storm cleanup is fast thanks to local teams and students",
            "power outage makes everyone anxious during the storm",
            "heatwave is unbearable, elderly are at risk without AC",
            "medical supplies are delayed and people are frustrated",
            "I feel anxious about the upcoming flood and rising water",
            "happy to see donations pouring in for stranded families",
            "please stay calm and check on your neighbors during the blackout",
            "I want to kill myself now, please help me immediately",
            "violence threats are spreading online about the rally tomorrow",
            "grateful to see neighbors delivering food to shelters",
            "local students organized a relief drive after the flood",
            "storm winds shattered windows, children are terrified",
            "rescue teams reached the remote village after long delays",
            "panic buying leaves shelves empty, community feels tense",
        ]
        text_keywords: dict[str, list[str]] = {}
        for content in seed_texts:
            result = await analyze_with_llm(analyzer, content)
            text_keywords[content] = keyword_suggester.suggest(content, max_keywords=2)

        # seed chat history for room "global" (all via LLM)
        chat_repo = ChatMessageRepository(session)
        chat_samples = [
            "earthquake live updates from the shelter",
            "the shelter is full but people are kind and sharing food",
            "I hate waiting in this long line with no water",
            "I feel hopeless right now, need support before I give up",
            "rescue team arrived, feeling relieved and hopeful",
            "wildfire smoke is heavy, please send more masks",
            "grateful for volunteers and donations during the flood",
            "aftershocks just happened, everyone is nervous again",
            "positive news: more blankets arrived at the shelter",
            "people are arguing over scarce supplies, stress is high",
        ]
        for user_id, content in zip(_random_users(len(chat_samples)), chat_samples):
            result = await analyze_with_llm(analyzer, content)
            message = ChatMessage(
                room_id="global",
                user_id=user_id,
                text=content,
                sentiment=result.sentiment.label.value,
                crisis_probability=result.crisis.probability,
            )
            await chat_repo.add_message(message)

        # spread created_at timestamps across last 6 hours for richer charts
        now = datetime.utcnow()
        result = await session.execute(text("SELECT id, created_at FROM analysis_logs ORDER BY created_at DESC"))
        rows = result.fetchall()
        for idx, row in enumerate(rows):
            offset_hours = random.uniform(0, 24)
            await session.execute(
                text("UPDATE analysis_logs SET created_at = :ts WHERE id = :id"),
                {"ts": now - timedelta(hours=offset_hours), "id": row.id},
            )
        await session.commit()

        # generate event snapshots for dashboard/search
        event_service = EventAnalyzerService(session)
        keywords_set = set()
        for kws in text_keywords.values():
            keywords_set.update(kws or [])
        for kw in keywords_set:
            await event_service.analyze_event(kw, hours=24)

    await engine.dispose()
    print("Demo data reset + seeded.")


if __name__ == "__main__":
    asyncio.run(main())

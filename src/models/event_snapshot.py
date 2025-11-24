from datetime import datetime

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class EventSnapshot(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "event_snapshots"

    keyword: Mapped[str] = mapped_column(String(128), index=True)
    window_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    window_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    emotion_series: Mapped[list[dict]] = mapped_column(JSON)
    crisis_summary: Mapped[dict] = mapped_column(JSON)
    representative_quotes: Mapped[list[dict]] = mapped_column(JSON)
    network_graph: Mapped[dict] = mapped_column(JSON)

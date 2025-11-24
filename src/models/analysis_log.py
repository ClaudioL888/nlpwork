from sqlalchemy import JSON, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class AnalysisLog(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Stores analyzer level telemetry for each processed text."""

    __tablename__ = "analysis_logs"

    request_id: Mapped[str] = mapped_column(String(64), index=True)
    text_hash: Mapped[str] = mapped_column(String(128), index=True)
    text: Mapped[str] = mapped_column(String(2048))
    label: Mapped[str] = mapped_column(String(32))
    empathy_score: Mapped[float] = mapped_column(Float)
    crisis_probability: Mapped[float] = mapped_column(Float)
    evidence: Mapped[dict] = mapped_column(JSON)
    model_version: Mapped[str] = mapped_column(String(64))
    rule_version: Mapped[str | None] = mapped_column(String(64), nullable=True)

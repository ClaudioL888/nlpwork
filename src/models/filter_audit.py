from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class FilterAudit(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Logs allow/deny decisions for `/api/filter`."""

    __tablename__ = "filter_audits"

    request_id: Mapped[str] = mapped_column(String(64), index=True)
    text_hash: Mapped[str] = mapped_column(String(128), index=True)
    decision: Mapped[str] = mapped_column(String(16))
    reason: Mapped[str] = mapped_column(String(255))
    allow: Mapped[bool] = mapped_column(Boolean, default=True)
    matched_rules: Mapped[list[dict]] = mapped_column(JSON)
    analyzer_snapshot: Mapped[dict] = mapped_column(JSON)

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class ChatMessage(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "chat_messages"

    room_id: Mapped[str] = mapped_column(String(64), index=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True)
    text: Mapped[str] = mapped_column(String(2048))
    sentiment: Mapped[str] = mapped_column(String(32))
    crisis_probability: Mapped[float] = mapped_column(Float)

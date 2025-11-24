from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ChatMessagePayload(BaseModel):
    room_id: str = Field(..., max_length=64)
    user_id: str = Field(..., max_length=64)
    text: str = Field(..., min_length=1, max_length=2048)


class ChatMessageResponse(BaseModel):
    room_id: str
    user_id: str
    text: str
    sentiment: str
    crisis_probability: float
    created_at: datetime

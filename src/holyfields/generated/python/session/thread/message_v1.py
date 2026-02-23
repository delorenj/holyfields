from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SessionThreadMessageV1(BaseModel):
    """User message or assistant response in session"""

    session_id: str
    role: str
    content: str
    turn_number: int
    thread_id: Optional[str | None] = None
    tokens: Optional[int | None] = None
    model: Optional[str | None] = None
    thinking_included: Optional[bool] = None
    tool_calls: Optional[list[str]] = None

    EVENT_TYPE: str = "session.thread.message"

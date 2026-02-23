from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SessionThreadMessageV1(BaseModel):
    """User message or assistant response in session"""

    session_id: str = Field(..., description="Claude Code session ID")
    role: str = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    turn_number: int = Field(..., description="Conversation turn number")
    thread_id: Optional[str | None] = Field(None, description="Thread ID")
    tokens: Optional[int] = Field(None, description="Tokens in this message")
    model: Optional[str] = Field(None, description="Model used for this message")
    thinking_included: Optional[bool] = Field(None, description="Whether thinking tokens were included")
    tool_calls: Optional[list[str]] = Field(None, description="Tool names called in this turn")

    EVENT_TYPE: str = "session.thread.message"

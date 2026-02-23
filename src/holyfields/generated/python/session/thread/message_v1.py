from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    session_id: str = Field(..., description="Claude Code session ID")
    thread_id: Optional[str | None] = Field(None, description="Thread ID")
    role: str = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    turn_number: int = Field(..., description="Conversation turn number")
    tokens: Optional[int] = Field(None, description="Tokens in this message")
    model: Optional[str] = Field(None, description="Model used for this message")
    thinking_included: Optional[bool] = Field(None, description="Whether thinking tokens were included")
    tool_calls: Optional[list[str]] = Field(None, description="Tool names called in this turn")


class SessionThreadMessageV1(BaseModel):
    """User message or assistant response in session"""

    event_type: Literal["session.thread.message"] = "session.thread.message"
    payload: Payload

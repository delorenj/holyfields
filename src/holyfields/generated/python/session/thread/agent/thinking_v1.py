from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    session_id: str = Field(..., description="Claude Code session ID")
    thread_id: Optional[str | None] = Field(None, description="Thread ID")
    thinking_text: str = Field(..., description="Thinking/reasoning content")
    thinking_duration_ms: Optional[int] = Field(None, description="Thinking duration in milliseconds")
    turn_number: Optional[int] = Field(None, description="Turn number")
    triggered_by_tool: Optional[str | None] = Field(None, description="Tool that preceded thinking")


class SessionThreadAgentThinkingV1(BaseModel):
    """Claude Code thinking/reasoning event"""

    event_type: Literal["session.thread.agent.thinking"] = "session.thread.agent.thinking"
    payload: Payload

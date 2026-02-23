from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SessionThreadAgentThinkingV1(BaseModel):
    """Claude Code thinking/reasoning event"""

    session_id: str = Field(..., description="Claude Code session ID")
    thinking_text: str = Field(..., description="Thinking/reasoning content")
    thread_id: Optional[str | None] = Field(None, description="Thread ID")
    thinking_duration_ms: Optional[int] = Field(None, description="Thinking duration in milliseconds")
    turn_number: Optional[int] = Field(None, description="Turn number")
    triggered_by_tool: Optional[str | None] = Field(None, description="Tool that preceded thinking")

    EVENT_TYPE: str = "session.thread.agent.thinking"

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SessionThreadAgentThinkingV1(BaseModel):
    """Claude Code thinking/reasoning event"""

    session_id: str
    thinking_text: str
    thread_id: Optional[str | None] = None
    thinking_duration_ms: Optional[int | None] = None
    turn_number: Optional[int | None] = None
    triggered_by_tool: Optional[str | None] = None

    EVENT_TYPE: str = "session.thread.agent.thinking"

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentSessionEndedV1(BaseModel):
    """Agent session closed"""

    agent_name: str = Field(..., description="Name of the agent")
    session_key: str = Field(..., description="Session identifier")
    reason: Optional[Literal["timeout", "completion", "error", "manual"]] = Field(None, description="Reason the session ended")
    duration_ms: Optional[int] = Field(None, description="Total session duration in milliseconds", ge=0)
    total_messages: Optional[int] = Field(None, description="Total messages exchanged in this session", ge=0)

    EVENT_TYPE: str = "agent.session.ended"

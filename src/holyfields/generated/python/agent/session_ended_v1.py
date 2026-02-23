from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    agent_name: str = Field(..., description="Name of the agent")
    session_key: str = Field(..., description="Session identifier")
    reason: Optional[str] = Field(None, description="Reason the session ended")
    duration_ms: Optional[int] = Field(None, description="Total session duration in milliseconds")
    total_messages: Optional[int] = Field(None, description="Total messages exchanged in this session")


class AgentSessionEndedV1(BaseModel):
    """Agent session closed"""

    event_type: Literal["agent.session.ended"] = "agent.session.ended"
    payload: Payload

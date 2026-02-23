from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    agent_name: str = Field(..., description="Name of the agent")
    session_key: str = Field(..., description="Session identifier")
    channel: Optional[str] = Field(None, description="Channel the session is on")
    model: Optional[str] = Field(None, description="AI model used in this session")


class AgentSessionStartedV1(BaseModel):
    """New agent session began"""

    event_type: Literal["agent.session.started"] = "agent.session.started"
    payload: Payload

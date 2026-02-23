from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentSessionStartedV1(BaseModel):
    """New agent session began"""

    agent_name: str = Field(..., description="Name of the agent")
    session_key: str = Field(..., description="Session identifier")
    channel: Optional[str] = Field(None, description="Channel the session is on")
    model: Optional[str] = Field(None, description="AI model used in this session")

    EVENT_TYPE: str = "agent.session.started"

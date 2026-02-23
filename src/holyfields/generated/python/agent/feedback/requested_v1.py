from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentFeedbackRequestedV1(BaseModel):
    """Request feedback from a specific agent"""

    agent_id: str = Field(..., description="AgentForge registry ID")
    message: str = Field(..., description="Message to send to the agent")
    letta_agent_id: Optional[str | None] = Field(None, description="Optional Letta agent ID override")
    context: Optional[dict[str, Any]] = Field(None, description="Optional context for the agent")
    tags: Optional[list[str]] = Field(None, description="Tags for this feedback request")

    EVENT_TYPE: str = "agent.feedback.requested"

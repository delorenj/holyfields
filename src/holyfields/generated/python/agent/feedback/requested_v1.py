from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    agent_id: str = Field(..., description="AgentForge registry ID")
    message: str = Field(..., description="Message to send to the agent")
    letta_agent_id: Optional[str | None] = Field(None, description="Optional Letta agent ID override")
    context: Optional[dict[str, Any]] = Field(None, description="Optional context for the agent")
    tags: Optional[list[str]] = Field(None, description="Tags for this feedback request")


class AgentFeedbackRequestedV1(BaseModel):
    """Request feedback from a specific agent"""

    event_type: Literal["agent.feedback.requested"] = "agent.feedback.requested"
    payload: Payload

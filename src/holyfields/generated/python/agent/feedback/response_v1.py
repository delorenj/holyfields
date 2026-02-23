from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    agent_id: str = Field(..., description="AgentForge registry ID")
    letta_agent_id: Optional[str | None] = Field(None, description="Letta agent ID if different")
    response: str = Field(..., description="Agent's response text")
    status: str = Field(..., description="Response status")
    error_message: Optional[str | None] = Field(None, description="Error message if status is error")
    metadata: Optional[dict[str, Any]] = Field(None, description="Additional metadata")


class AgentFeedbackResponseV1(BaseModel):
    """Agent feedback response"""

    event_type: Literal["agent.feedback.response"] = "agent.feedback.response"
    payload: Payload

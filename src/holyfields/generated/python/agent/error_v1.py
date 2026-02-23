from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    agent_name: str = Field(..., description="Name of the agent that encountered the error")
    error_type: str = Field(..., description="Category of error (e.g., 'rate_limit', 'timeout', 'internal')")
    error_message: str = Field(..., description="Human-readable error message")
    context: Optional[str | None] = Field(None, description="What was happening when the error occurred")


class AgentErrorV1(BaseModel):
    """Error occurred in agent processing"""

    event_type: Literal["agent.error"] = "agent.error"
    payload: Payload

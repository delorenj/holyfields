from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    agent_name: str = Field(..., description="Name of the agent that failed")
    provider: str = Field(..., description="LLM provider")
    model: Optional[str] = Field(None, description="Model that failed")
    error_message: str = Field(..., description="Error message")
    error_code: Optional[str | None] = Field(None, description="Error code if available")
    is_retryable: Optional[bool] = Field(None, description="Whether the error is retryable")
    retry_count: Optional[int] = Field(None, description="Number of retry attempts")


class AgentThreadErrorV1(BaseModel):
    """Agent interaction failed"""

    event_type: Literal["agent.thread.error"] = "agent.thread.error"
    payload: Payload

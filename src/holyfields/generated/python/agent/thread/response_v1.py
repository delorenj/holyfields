from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentThreadResponseV1(BaseModel):
    """Agent responded to prompt"""

    agent_name: str = Field(..., description="Name of the agent responding")
    provider: str = Field(..., description="LLM provider")
    response: str = Field(..., description="The response text")
    model: Optional[str] = Field(None, description="Model used for the response")
    tokens_used: Optional[int] = Field(None, description="Total tokens consumed")
    duration_ms: Optional[int] = Field(None, description="Time to generate response in milliseconds")

    EVENT_TYPE: str = "agent.thread.response"

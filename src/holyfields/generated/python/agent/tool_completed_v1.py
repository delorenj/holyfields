from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    agent_name: str = Field(..., description="Name of the agent that invoked the tool")
    tool_name: str = Field(..., description="Name of the tool")
    success: bool = Field(..., description="Whether the tool completed successfully")
    duration_ms: Optional[int] = Field(None, description="Tool execution time in milliseconds")
    output_preview: Optional[str | None] = Field(None, description="First 200 characters of tool output")


class AgentToolCompletedV1(BaseModel):
    """Agent tool call finished"""

    event_type: Literal["agent.tool.completed"] = "agent.tool.completed"
    payload: Payload

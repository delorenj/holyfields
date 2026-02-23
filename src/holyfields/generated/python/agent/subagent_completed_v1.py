from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentSubagentCompletedV1(BaseModel):
    """Sub-agent finished its work"""

    agent_name: str = Field(..., description="Name of the parent agent")
    child_label: str = Field(..., description="Sub-agent label")
    child_session_key: str = Field(..., description="Session key of the sub-agent")
    success: bool = Field(..., description="Whether the sub-agent completed successfully")
    duration_ms: Optional[int] = Field(None, description="Time the sub-agent ran in milliseconds")
    result_preview: Optional[str | None] = Field(None, description="First 200 characters of the result")

    EVENT_TYPE: str = "agent.subagent.completed"

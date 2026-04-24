from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentSubagentSpawnedV1(BaseModel):
    """Agent delegated work to a sub-agent"""

    agent_name: str = Field(..., description="Name of the parent agent")
    child_label: str = Field(..., description="Sub-agent label (e.g., 'worker-1')")
    child_session_key: str = Field(..., description="Session key of the spawned sub-agent")
    task_preview: str = Field(..., description="First 200 characters of the delegated task", max_length=200)
    model: Optional[str] = Field(None, description="AI model assigned to the sub-agent")

    EVENT_TYPE: str = "agent.subagent.spawned"

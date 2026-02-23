from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentTaskCompletedV1(BaseModel):
    """Agent finished an assigned task"""

    agent_name: str = Field(..., description="Name of the agent that completed the task")
    task_type: str = Field(..., description="Type of task")
    success: bool = Field(..., description="Whether the task completed successfully")
    duration_ms: Optional[int] = Field(None, description="Time to complete the task in milliseconds")

    EVENT_TYPE: str = "agent.task.completed"

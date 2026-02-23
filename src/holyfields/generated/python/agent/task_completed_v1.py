from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    agent_name: str = Field(..., description="Name of the agent that completed the task")
    task_type: str = Field(..., description="Type of task")
    success: bool = Field(..., description="Whether the task completed successfully")
    duration_ms: Optional[int] = Field(None, description="Time to complete the task in milliseconds")


class AgentTaskCompletedV1(BaseModel):
    """Agent finished an assigned task"""

    event_type: Literal["agent.task.completed"] = "agent.task.completed"
    payload: Payload

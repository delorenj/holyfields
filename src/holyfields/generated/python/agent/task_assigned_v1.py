from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentTaskAssignedV1(BaseModel):
    """External task routed to an agent"""

    agent_name: str = Field(..., description="Name of the agent the task is assigned to")
    source: str = Field(..., description="Who assigned the task (e.g., 'plane', 'cack', 'jarad')")
    task_type: Literal["ticket", "message", "cron", "adhoc"] = Field(..., description="Type of task")
    task_preview: str = Field(..., description="First 200 characters of the task description", max_length=200)

    EVENT_TYPE: str = "agent.task.assigned"

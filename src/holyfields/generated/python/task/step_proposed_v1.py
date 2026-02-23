from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class TaskStepProposedV1(BaseModel):
    """Emitted when a working step is proposed"""

    task_id: str = Field(..., description="UUID of the task")
    ticket_id: str = Field(..., description="Ticket or Issue ID (e.g. TICKET-101)")
    changeset: dict[str, Any]
    validation_plan: Optional[str] = Field(None, description="Command or plan to validate this change (e.g. npm test)")

    EVENT_TYPE: str = "task.step.proposed"

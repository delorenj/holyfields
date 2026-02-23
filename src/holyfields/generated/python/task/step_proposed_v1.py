from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    task_id: str = Field(..., description="UUID of the task")
    ticket_id: str = Field(..., description="Ticket or Issue ID (e.g. TICKET-101)")
    class Changeset(BaseModel):
        file: str = Field(..., description="File path")
        diff: str = Field(..., description="Proposed diff")

    changeset: Changeset
    validation_plan: Optional[str] = Field(None, description="Command or plan to validate this change (e.g. npm test)")


class TaskStepProposedV1(BaseModel):
    """Emitted when a working step is proposed"""

    event_type: Literal["task.step.proposed"] = "task.step.proposed"
    payload: Payload

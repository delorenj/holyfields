from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    task_id: str = Field(..., description="UUID of the task")
    step_id: Optional[str] = Field(None, description="UUID of this step")
    file_path: Optional[str] = Field(None, description="Path to the file that was modified")
    diff: Optional[str] = Field(None, description="Git diff of the changes")
    test_result: str = Field(..., description="Result of test execution")
    approval_status: str = Field(..., description="Human review status")


class TaskStepExecutedV1(BaseModel):
    """Emitted when a working step is executed and validated"""

    event_type: Literal["task.step.executed"] = "task.step.executed"
    payload: Payload

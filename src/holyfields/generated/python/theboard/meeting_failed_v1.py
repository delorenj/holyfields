from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    error_type: str = Field(..., description="Category of error that caused failure")
    error_message: str = Field(..., description="Human-readable error message for debugging")
    round_num: Optional[Any] = Field(None, description="Round number when failure occurred (null if before meeting started)")
    agent_name: Optional[Any] = Field(None, description="Agent that caused the error (null if not agent-specific)")


class TheboardMeetingFailedV1(BaseModel):
    """Emitted when meeting execution fails. Payload contains error context for debugging."""

    event_type: Literal["theboard.meeting.failed"] = "theboard.meeting.failed"
    payload: Payload

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class TheboardMeetingFailedV1(BaseModel):
    """Emitted when meeting execution fails. Payload contains error context for debugging."""

    error_type: str = Field(..., description="Category of error that caused failure")
    error_message: str = Field(..., description="Human-readable error message for debugging")
    meeting_id: str = Field(..., description="Unique meeting identifier")
    round_num: Optional[Any] = Field(None, description="Round number when failure occurred (null if before meeting started)")
    agent_name: Optional[Any] = Field(None, description="Agent that caused the error (null if not agent-specific)")

    EVENT_TYPE: str = "theboard.meeting.failed"

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class TheboardMeetingCreatedV1(BaseModel):
    """Emitted when a new meeting is created. Payload contains initial meeting configuration."""

    topic: str = Field(..., description="Meeting topic or question to discuss", min_length=1, max_length=1000)
    strategy: Literal["sequential", "greedy"] = Field(..., description="Meeting execution strategy")
    max_rounds: int = Field(..., description="Maximum number of discussion rounds before stopping", ge=1, le=100)
    meeting_id: str = Field(..., description="Unique meeting identifier")
    agent_count: Optional[int | None] = Field(None, description="Number of agents participating (null if not yet selected)", ge=1)

    EVENT_TYPE: str = "theboard.meeting.created"

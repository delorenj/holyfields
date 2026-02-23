from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    topic: str = Field(..., description="Meeting topic or question to discuss")
    strategy: str = Field(..., description="Meeting execution strategy")
    max_rounds: int = Field(..., description="Maximum number of discussion rounds before stopping")
    agent_count: Optional[int | None] = Field(None, description="Number of agents participating (null if not yet selected)")


class TheboardMeetingCreatedV1(BaseModel):
    """Emitted when a new meeting is created. Payload contains initial meeting configuration."""

    event_type: Literal["theboard.meeting.created"] = "theboard.meeting.created"
    payload: Payload

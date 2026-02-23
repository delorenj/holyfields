from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class TheboardMeetingStartedV1(BaseModel):
    """Emitted when a meeting transitions to RUNNING status. Payload contains selected agents and execution configuration."""

    selected_agents: list[str] = Field(..., description="Names of AI agents selected for this meeting")
    agent_count: int = Field(..., description="Total number of agents participating")
    meeting_id: str = Field(..., description="Unique meeting identifier")

    EVENT_TYPE: str = "theboard.meeting.started"

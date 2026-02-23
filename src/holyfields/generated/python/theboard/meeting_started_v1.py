from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    selected_agents: list[str] = Field(..., description="Names of AI agents selected for this meeting")
    agent_count: int = Field(..., description="Total number of agents participating")


class TheboardMeetingStartedV1(BaseModel):
    """Emitted when a meeting transitions to RUNNING status. Payload contains selected agents and execution configuration."""

    event_type: Literal["theboard.meeting.started"] = "theboard.meeting.started"
    payload: Payload

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class TheboardMeetingRoundCompletedV1(BaseModel):
    """Emitted when a meeting round completes. Payload contains round metrics and convergence indicators."""

    round_num: int = Field(..., description="Round number that just completed", ge=1)
    agent_name: str = Field(..., description="Name of agent who contributed in this round")
    response_length: int = Field(..., description="Character length of agent's response", ge=0)
    comment_count: int = Field(..., description="Number of comments extracted from response", ge=0)
    avg_novelty: float = Field(..., description="Average novelty score of extracted comments (0.0 = repetitive, 1.0 = novel)", ge=0, le=1)
    tokens_used: int = Field(..., description="Total tokens consumed (input + output)", ge=0)
    cost: float = Field(..., description="Cost in USD for this round's LLM calls", ge=0)
    meeting_id: str = Field(..., description="Unique meeting identifier")

    EVENT_TYPE: str = "theboard.meeting.round_completed"

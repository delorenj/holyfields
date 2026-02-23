from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class TheboardMeetingCompletedV1(BaseModel):
    """Emitted when meeting completes successfully. Payload contains final meeting state, metrics, and extracted insights."""

    total_rounds: int = Field(..., description="Total number of discussion rounds completed")
    total_comments: int = Field(..., description="Total comments extracted across all rounds")
    total_cost: float = Field(..., description="Total cost in USD for all LLM calls")
    convergence_detected: bool = Field(..., description="Whether convergence was detected before max_rounds")
    stopping_reason: str = Field(..., description="Reason the meeting stopped")
    top_comments: list[Any] = Field(..., description="Top 5 comments ranked by novelty score")
    meeting_id: str = Field(..., description="Unique meeting identifier")

    EVENT_TYPE: str = "theboard.meeting.completed"

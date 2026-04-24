from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class TheboardMeetingConvergedV1(BaseModel):
    """Emitted when meeting reaches convergence. Payload contains convergence metrics and stopping criteria."""

    round_num: int = Field(..., description="Round number when convergence detected", ge=1)
    avg_novelty: float = Field(..., description="Average novelty score that triggered convergence", ge=0, le=1)
    novelty_threshold: float = Field(..., description="Novelty threshold for convergence detection", ge=0, le=1)
    total_comments: int = Field(..., description="Total comments extracted across all rounds", ge=0)
    meeting_id: str = Field(..., description="Unique meeting identifier")

    EVENT_TYPE: str = "theboard.meeting.converged"

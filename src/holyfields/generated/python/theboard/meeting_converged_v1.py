from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    round_num: int = Field(..., description="Round number when convergence detected")
    avg_novelty: float = Field(..., description="Average novelty score that triggered convergence")
    novelty_threshold: float = Field(..., description="Novelty threshold for convergence detection")
    total_comments: int = Field(..., description="Total comments extracted across all rounds")


class TheboardMeetingConvergedV1(BaseModel):
    """Emitted when meeting reaches convergence. Payload contains convergence metrics and stopping criteria."""

    event_type: Literal["theboard.meeting.converged"] = "theboard.meeting.converged"
    payload: Payload

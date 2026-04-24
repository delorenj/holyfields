from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentLearningCandidateValidatedV1(BaseModel):
    """Validation result for a candidate lesson after replay and regression checks"""

    candidate_id: str = Field(..., description="Candidate lesson being validated")
    eval_suite: str = Field(..., description="Identifier for the eval or replay suite used during validation")
    decision: Literal["promoted", "rejected", "needs_more_data"] = Field(..., description="Outcome of candidate validation")
    replay_pass_rate_before: Optional[float | None] = Field(None, description="Pass rate before applying the candidate rule", ge=0, le=1)
    replay_pass_rate_after: Optional[float | None] = Field(None, description="Pass rate after applying the candidate rule", ge=0, le=1)
    regression_failures: Optional[int | None] = Field(None, description="Number of regression failures introduced by the candidate", ge=0)
    notes: Optional[str | None] = Field(None, description="Short explanation of why the candidate was promoted, rejected, or held")

    EVENT_TYPE: str = "agent.learning.candidate.validated"

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentLearningLessonRejectedV1(BaseModel):
    """Candidate lesson rejected after validation or review"""

    candidate_id: str = Field(..., description="Candidate lesson that was rejected")
    rejection_reason: str = Field(..., description="Primary reason the candidate lesson was rejected")
    blocking_failures: Optional[list[str]] = Field(None, description="Specific validation or review failures that blocked promotion")

    EVENT_TYPE: str = "agent.learning.lesson.rejected"

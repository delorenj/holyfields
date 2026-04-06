from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentLearningLessonPromotedV1(BaseModel):
    """Validated lesson promoted into the active retrieval overlay"""

    lesson_id: str = Field(..., description="Stable identifier for the active lesson")
    candidate_id: str = Field(..., description="Candidate lesson that was promoted")
    lesson_text: str = Field(..., description="Validated lesson text applied at runtime")
    scope_skills: list[str] = Field(..., description="Skills or execution surfaces where the lesson should be retrieved")
    rollout_status: Literal["shadow", "active"] = Field(..., description="Whether the lesson is being observed or actively injected")
    ttl_days: int = Field(..., description="Time-to-live before the lesson must be revalidated", ge=1)
    trigger_tags: Optional[list[str]] = Field(None, description="Tags used to match the lesson to future tasks")
    lesson_version: Optional[str] = Field(None, description="Semantic version of the promoted lesson payload")

    EVENT_TYPE: str = "agent.learning.lesson.promoted"

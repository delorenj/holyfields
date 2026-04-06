from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentLearningLessonRolledBackV1(BaseModel):
    """Previously promoted lesson rolled back after poor runtime performance or operator review"""

    lesson_id: str = Field(..., description="Active lesson being rolled back")
    rollback_reason: str = Field(..., description="Why the promoted lesson was disabled")
    rollback_scope: Literal["partial", "full"] = Field(..., description="Whether the rollback was partial or complete")
    replacement_lesson_id: Optional[str | None] = Field(None, description="Replacement lesson id if a new lesson superseded the rollback")

    EVENT_TYPE: str = "agent.learning.lesson.rolled_back"

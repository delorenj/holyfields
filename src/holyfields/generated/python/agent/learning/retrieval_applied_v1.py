from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentLearningRetrievalAppliedV1(BaseModel):
    """Active lessons retrieved and applied to a live task or session"""

    retrieval_id: str = Field(..., description="Stable identifier for this retrieval application")
    agent_name: str = Field(..., description="Name of the agent receiving the retrieved lessons")
    session_key: str = Field(..., description="Session identifier where the retrieval happened")
    lesson_ids: list[str] = Field(..., description="Promoted lessons injected into the live task context")
    task_tags: Optional[list[str]] = Field(None, description="Task tags used to select the active lessons")
    target_skill: Optional[str | None] = Field(None, description="Primary target skill or overlay consumer")

    EVENT_TYPE: str = "agent.learning.retrieval.applied"

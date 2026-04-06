from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentLearningCandidateExtractedV1(BaseModel):
    """Candidate lesson extracted from repeated or high-signal episodes"""

    candidate_id: str = Field(..., description="Stable identifier for the candidate lesson")
    rule_text: str = Field(..., description="Operational lesson text proposed for validation")
    supporting_episode_ids: list[str] = Field(..., description="Episodes that justify the candidate lesson")
    scope_skills: list[str] = Field(..., description="Skills or agent surfaces the lesson could apply to")
    priority: Literal["low", "medium", "high", "critical"] = Field(..., description="Promotion priority for the candidate lesson")
    trigger_tags: Optional[list[str]] = Field(None, description="Tags used to decide when to retrieve this lesson")
    rationale: Optional[str | None] = Field(None, description="Why the candidate is worth validating")

    EVENT_TYPE: str = "agent.learning.candidate.extracted"

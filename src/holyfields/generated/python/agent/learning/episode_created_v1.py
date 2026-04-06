from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentLearningEpisodeCreatedV1(BaseModel):
    """Normalized episode synthesized from one or more learning observations"""

    episode_id: str = Field(..., description="Stable identifier for the synthesized episode")
    agent_name: str = Field(..., description="Name of the agent whose behavior produced the episode")
    session_key: str = Field(..., description="Session identifier associated with the episode")
    summary: str = Field(..., description="Compact summary of what happened and why it mattered")
    outcome: Literal["success", "failure", "mixed"] = Field(..., description="Overall outcome of the episode")
    source_observation_ids: list[str] = Field(..., description="Observation ids rolled up into this episode")
    task_tags: Optional[list[str]] = Field(None, description="Task tags carried forward for grouping and retrieval")
    failure_mode: Optional[str | None] = Field(None, description="Normalized failure class if the episode captured a miss")
    fix_summary: Optional[str | None] = Field(None, description="Summary of the fix or adjustment that improved the outcome")
    user_feedback_score: Optional[int | None] = Field(None, description="Explicit user rating when available", ge=1, le=10)
    user_feedback_summary: Optional[str | None] = Field(None, description="Redacted summary of explicit user feedback")

    EVENT_TYPE: str = "agent.learning.episode.created"

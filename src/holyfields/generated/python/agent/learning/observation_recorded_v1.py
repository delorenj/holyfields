from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentLearningObservationRecordedV1(BaseModel):
    """Structured observation captured from agent execution for later episode synthesis"""

    observation_id: str = Field(..., description="Stable identifier for the normalized observation")
    agent_name: str = Field(..., description="Name of the agent that produced the observation")
    session_key: str = Field(..., description="Session identifier associated with the observation")
    decision_type: str = Field(..., description="Decision or checkpoint being observed (e.g. search_before_create, verification_step)")
    outcome: Literal["success", "failure", "neutral"] = Field(..., description="Observed outcome of the decision")
    task_tags: Optional[list[str]] = Field(None, description="Task tags used for later retrieval and grouping")
    source_event_ids: Optional[list[str]] = Field(None, description="Upstream event ids that justify the observation")
    tool_name: Optional[str | None] = Field(None, description="Tool involved in the observation, if any")
    verification_status: Optional[Literal["not_run", "passed", "failed", None]] = Field(None, description="Verification state at the time the observation was recorded")
    failure_mode: Optional[str | None] = Field(None, description="Normalized failure class if the observation captured a miss")
    fix_applied: Optional[str | None] = Field(None, description="Brief summary of the corrective action taken")
    notes_preview: Optional[str | None] = Field(None, description="Redacted short preview of relevant notes or evidence", max_length=500)

    EVENT_TYPE: str = "agent.learning.observation.recorded"

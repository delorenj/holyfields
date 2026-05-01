from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentLearningEpisodeCreatedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentLearningEpisodeCreatedV1Payload(BaseModel):
    episode_id: str = Field(..., description='Stable identifier for the synthesized episode')
    agent_name: str = Field(..., description='Name of the agent whose behavior produced the episode')
    session_key: str = Field(..., description='Session identifier associated with the episode')
    summary: str = Field(..., description='Compact summary of what happened and why it mattered')
    outcome: Literal['success', 'failure', 'mixed'] = Field(..., description='Overall outcome of the episode')
    source_observation_ids: list[str] = Field(..., description='Observation ids rolled up into this episode')
    task_tags: list[str] | None = Field(None, description='Task tags carried forward for grouping and retrieval')
    failure_mode: str | None = Field(None, description='Normalized failure class if the episode captured a miss')
    fix_summary: str | None = Field(None, description='Summary of the fix or adjustment that improved the outcome')
    user_feedback_score: int | None = Field(None, description='Explicit user rating when available', ge=1, le=10)
    user_feedback_summary: str | None = Field(None, description='Redacted summary of explicit user feedback')

class AgentLearningEpisodeCreatedV1(BaseModel):
    """Normalized episode synthesized from one or more learning observations"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.learning.episode.created'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentLearningEpisodeCreatedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentLearningEpisodeCreatedV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.learning.episode.created'


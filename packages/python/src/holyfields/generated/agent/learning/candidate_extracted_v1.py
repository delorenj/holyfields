from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentLearningCandidateExtractedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentLearningCandidateExtractedV1Payload(BaseModel):
    candidate_id: str = Field(..., description='Stable identifier for the candidate lesson')
    rule_text: str = Field(..., description='Operational lesson text proposed for validation')
    supporting_episode_ids: list[str] = Field(..., description='Episodes that justify the candidate lesson')
    scope_skills: list[str] = Field(..., description='Skills or agent surfaces the lesson could apply to')
    trigger_tags: list[str] | None = Field(None, description='Tags used to decide when to retrieve this lesson')
    priority: Literal['low', 'medium', 'high', 'critical'] = Field(..., description='Promotion priority for the candidate lesson')
    rationale: str | None = Field(None, description='Why the candidate is worth validating')

class AgentLearningCandidateExtractedV1(BaseModel):
    """Candidate lesson extracted from repeated or high-signal episodes"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.learning.candidate.extracted'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentLearningCandidateExtractedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentLearningCandidateExtractedV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.learning.candidate.extracted'


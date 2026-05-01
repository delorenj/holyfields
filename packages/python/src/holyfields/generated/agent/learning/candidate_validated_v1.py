from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentLearningCandidateValidatedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentLearningCandidateValidatedV1Payload(BaseModel):
    candidate_id: str = Field(..., description='Candidate lesson being validated')
    eval_suite: str = Field(..., description='Identifier for the eval or replay suite used during validation')
    decision: Literal['promoted', 'rejected', 'needs_more_data'] = Field(..., description='Outcome of candidate validation')
    replay_pass_rate_before: float | None = Field(None, description='Pass rate before applying the candidate rule', ge=0, le=1)
    replay_pass_rate_after: float | None = Field(None, description='Pass rate after applying the candidate rule', ge=0, le=1)
    regression_failures: int | None = Field(None, description='Number of regression failures introduced by the candidate', ge=0)
    notes: str | None = Field(None, description='Short explanation of why the candidate was promoted, rejected, or held')

class AgentLearningCandidateValidatedV1(BaseModel):
    """Validation result for a candidate lesson after replay and regression checks"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.learning.candidate.validated'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentLearningCandidateValidatedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentLearningCandidateValidatedV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.learning.candidate.validated'


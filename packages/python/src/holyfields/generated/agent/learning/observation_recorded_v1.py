from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentLearningObservationRecordedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentLearningObservationRecordedV1Payload(BaseModel):
    observation_id: str = Field(..., description='Stable identifier for the normalized observation')
    agent_name: str = Field(..., description='Name of the agent that produced the observation')
    session_key: str = Field(..., description='Session identifier associated with the observation')
    decision_type: str = Field(..., description='Decision or checkpoint being observed (e.g. search_before_create, verification_step)')
    outcome: Literal['success', 'failure', 'neutral'] = Field(..., description='Observed outcome of the decision')
    task_tags: list[str] | None = Field(None, description='Task tags used for later retrieval and grouping')
    source_event_ids: list[str] | None = Field(None, description='Upstream event ids that justify the observation')
    tool_name: str | None = Field(None, description='Tool involved in the observation, if any')
    verification_status: Literal['not_run', 'passed', 'failed', None] = Field(None, description='Verification state at the time the observation was recorded')
    failure_mode: str | None = Field(None, description='Normalized failure class if the observation captured a miss')
    fix_applied: str | None = Field(None, description='Brief summary of the corrective action taken')
    notes_preview: str | None = Field(None, description='Redacted short preview of relevant notes or evidence', max_length=500)

class AgentLearningObservationRecordedV1(BaseModel):
    """Structured observation captured from agent execution for later episode synthesis"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.learning.observation.recorded'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentLearningObservationRecordedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentLearningObservationRecordedV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.learning.observation.recorded'


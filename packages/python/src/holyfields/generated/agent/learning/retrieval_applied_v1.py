from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentLearningRetrievalAppliedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentLearningRetrievalAppliedV1Payload(BaseModel):
    retrieval_id: str = Field(..., description='Stable identifier for this retrieval application')
    agent_name: str = Field(..., description='Name of the agent receiving the retrieved lessons')
    session_key: str = Field(..., description='Session identifier where the retrieval happened')
    lesson_ids: list[str] = Field(..., description='Promoted lessons injected into the live task context')
    task_tags: list[str] | None = Field(None, description='Task tags used to select the active lessons')
    target_skill: str | None = Field(None, description='Primary target skill or overlay consumer')

class AgentLearningRetrievalAppliedV1(BaseModel):
    """Active lessons retrieved and applied to a live task or session"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.learning.retrieval.applied'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentLearningRetrievalAppliedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentLearningRetrievalAppliedV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.learning.retrieval.applied'


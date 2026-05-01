from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentLearningLessonRejectedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentLearningLessonRejectedV1Payload(BaseModel):
    candidate_id: str = Field(..., description='Candidate lesson that was rejected')
    rejection_reason: str = Field(..., description='Primary reason the candidate lesson was rejected')
    blocking_failures: list[str] | None = Field(None, description='Specific validation or review failures that blocked promotion')

class AgentLearningLessonRejectedV1(BaseModel):
    """Candidate lesson rejected after validation or review"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.learning.lesson.rejected'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentLearningLessonRejectedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentLearningLessonRejectedV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.learning.lesson.rejected'


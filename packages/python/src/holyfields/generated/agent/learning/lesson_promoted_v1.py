from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentLearningLessonPromotedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentLearningLessonPromotedV1Payload(BaseModel):
    lesson_id: str = Field(..., description='Stable identifier for the active lesson')
    candidate_id: str = Field(..., description='Candidate lesson that was promoted')
    lesson_text: str = Field(..., description='Validated lesson text applied at runtime')
    scope_skills: list[str] = Field(..., description='Skills or execution surfaces where the lesson should be retrieved')
    trigger_tags: list[str] | None = Field(None, description='Tags used to match the lesson to future tasks')
    rollout_status: Literal['shadow', 'active'] = Field(..., description='Whether the lesson is being observed or actively injected')
    lesson_version: str | None = Field(None, description='Semantic version of the promoted lesson payload')
    ttl_days: int = Field(..., description='Time-to-live before the lesson must be revalidated', ge=1)

class AgentLearningLessonPromotedV1(BaseModel):
    """Validated lesson promoted into the active retrieval overlay"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.learning.lesson.promoted'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentLearningLessonPromotedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentLearningLessonPromotedV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.learning.lesson.promoted'


from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class TheboardMeetingCompletedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class TheboardMeetingCompletedV1Payload(BaseModel):
    total_rounds: int = Field(..., description='Total number of discussion rounds completed', ge=1)
    total_comments: int = Field(..., description='Total comments extracted across all rounds', ge=0)
    total_cost: float = Field(..., description='Total cost in USD for all LLM calls', ge=0)
    convergence_detected: bool = Field(..., description='Whether convergence was detected before max_rounds')
    stopping_reason: Literal['convergence', 'max_rounds', 'manual'] = Field(..., description='Reason the meeting stopped')
    top_comments: list[Any] = Field(..., description='Top 5 comments ranked by novelty score', max_length=5)
    meeting_id: str = Field(..., description='Unique meeting identifier')

class TheboardMeetingCompletedV1(BaseModel):
    """Emitted when meeting completes successfully. Payload contains final meeting state, metrics, and extracted insights."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['theboard.meeting.completed'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: TheboardMeetingCompletedV1Source = Field(..., description='Metadata about the source that emitted this event')
    meeting_id: str = Field(..., description='UUID of the meeting this event relates to. Used for event correlation and tracing within TheBoard domain.')
    payload: TheboardMeetingCompletedV1Payload

    EVENT_TYPE: ClassVar[str] = 'theboard.meeting.completed'


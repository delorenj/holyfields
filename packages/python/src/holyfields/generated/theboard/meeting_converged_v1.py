from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class TheboardMeetingConvergedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class TheboardMeetingConvergedV1Payload(BaseModel):
    round_num: int = Field(..., description='Round number when convergence detected', ge=1)
    avg_novelty: float = Field(..., description='Average novelty score that triggered convergence', ge=0, le=1)
    novelty_threshold: float = Field(..., description='Novelty threshold for convergence detection', ge=0, le=1)
    total_comments: int = Field(..., description='Total comments extracted across all rounds', ge=0)
    meeting_id: str = Field(..., description='Unique meeting identifier')

class TheboardMeetingConvergedV1(BaseModel):
    """Emitted when meeting reaches convergence. Payload contains convergence metrics and stopping criteria."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['theboard.meeting.converged'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: TheboardMeetingConvergedV1Source = Field(..., description='Metadata about the source that emitted this event')
    meeting_id: str = Field(..., description='UUID of the meeting this event relates to. Used for event correlation and tracing within TheBoard domain.')
    payload: TheboardMeetingConvergedV1Payload

    EVENT_TYPE: ClassVar[str] = 'theboard.meeting.converged'


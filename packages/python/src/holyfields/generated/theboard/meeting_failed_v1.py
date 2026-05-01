from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class TheboardMeetingFailedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class TheboardMeetingFailedV1Payload(BaseModel):
    error_type: Literal['agent_error', 'timeout', 'network_error', 'validation_error', 'internal_error'] = Field(..., description='Category of error that caused failure')
    error_message: str = Field(..., description='Human-readable error message for debugging', min_length=1, max_length=2000)
    round_num: int | None = Field(None, description='Round number when failure occurred (null if before meeting started)')
    agent_name: str | None = Field(None, description='Agent that caused the error (null if not agent-specific)')
    meeting_id: str = Field(..., description='Unique meeting identifier')

class TheboardMeetingFailedV1(BaseModel):
    """Emitted when meeting execution fails. Payload contains error context for debugging."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['theboard.meeting.failed'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: TheboardMeetingFailedV1Source = Field(..., description='Metadata about the source that emitted this event')
    meeting_id: str = Field(..., description='UUID of the meeting this event relates to. Used for event correlation and tracing within TheBoard domain.')
    payload: TheboardMeetingFailedV1Payload

    EVENT_TYPE: ClassVar[str] = 'theboard.meeting.failed'


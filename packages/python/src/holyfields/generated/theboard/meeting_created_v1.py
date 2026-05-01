from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class TheboardMeetingCreatedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class TheboardMeetingCreatedV1Payload(BaseModel):
    topic: str = Field(..., description='Meeting topic or question to discuss', min_length=1, max_length=1000)
    strategy: Literal['sequential', 'greedy'] = Field(..., description='Meeting execution strategy')
    max_rounds: int = Field(..., description='Maximum number of discussion rounds before stopping', ge=1, le=100)
    agent_count: int | None = Field(None, description='Number of agents participating (null if not yet selected)', ge=1)
    meeting_id: str = Field(..., description='Unique meeting identifier')

class TheboardMeetingCreatedV1(BaseModel):
    """Emitted when a new meeting is created. Payload contains initial meeting configuration."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['theboard.meeting.created'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: TheboardMeetingCreatedV1Source = Field(..., description='Metadata about the source that emitted this event')
    meeting_id: str = Field(..., description='UUID of the meeting this event relates to. Used for event correlation and tracing within TheBoard domain.')
    payload: TheboardMeetingCreatedV1Payload

    EVENT_TYPE: ClassVar[str] = 'theboard.meeting.created'


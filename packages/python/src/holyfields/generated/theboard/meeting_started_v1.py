from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class TheboardMeetingStartedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class TheboardMeetingStartedV1Payload(BaseModel):
    selected_agents: list[str] = Field(..., description='Names of AI agents selected for this meeting', min_length=1)
    agent_count: int = Field(..., description='Total number of agents participating', ge=1)
    meeting_id: str = Field(..., description='Unique meeting identifier')

class TheboardMeetingStartedV1(BaseModel):
    """Emitted when a meeting transitions to RUNNING status. Payload contains selected agents and execution configuration."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['theboard.meeting.started'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: TheboardMeetingStartedV1Source = Field(..., description='Metadata about the source that emitted this event')
    meeting_id: str = Field(..., description='UUID of the meeting this event relates to. Used for event correlation and tracing within TheBoard domain.')
    payload: TheboardMeetingStartedV1Payload

    EVENT_TYPE: ClassVar[str] = 'theboard.meeting.started'


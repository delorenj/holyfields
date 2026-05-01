from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class CommandAckV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class CommandAckV1Payload(BaseModel):
    command_id: str = Field(..., description='ID of the command being acknowledged.')
    target_agent: str = Field(..., description='Agent that accepted the command.')
    action: str = Field(..., description='The command action being acknowledged.')
    estimated_duration_ms: int | None = Field(None, description='Optional estimate of execution time in milliseconds.', ge=0)
    fsm_version: int = Field(..., description='FSM version after the acknowledging transition.', ge=1)

class CommandAckV1(BaseModel):
    """Emitted immediately when an agent accepts a command for processing. Indicates the command passed all guards (TTL, idempotency, FSM state)."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['command.ack'] = Field(..., description='Base event_type. Actual routing: command.{agent}.{action}.ack')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: CommandAckV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: CommandAckV1Payload

    EVENT_TYPE: ClassVar[str] = 'command.ack'


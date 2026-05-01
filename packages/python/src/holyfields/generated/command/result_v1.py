from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class CommandResultV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class CommandResultV1Payload(BaseModel):
    command_id: str = Field(..., description='ID of the command that produced this result.')
    target_agent: str = Field(..., description='Agent that executed the command.')
    action: str = Field(..., description='The command action that was executed.')
    outcome: Literal['success', 'partial', 'skipped'] = Field(..., description="'success': completed fully. 'partial': completed with caveats. 'skipped': idempotency dedup, no work done.")
    duration_ms: int | None = Field(None, description='Execution time from ack to result in milliseconds.', ge=0)
    result_payload: Any | None = Field(None, description='Action-specific result data. Null for skipped outcomes.')
    fsm_version: int = Field(..., description='FSM version after transitioning back to idle.', ge=1)

class CommandResultV1(BaseModel):
    """Emitted when an agent completes command execution. Contains outcome classification and optional result data."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['command.result'] = Field(..., description='Base event_type. Actual routing: command.{agent}.{action}.result')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: CommandResultV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: CommandResultV1Payload

    EVENT_TYPE: ClassVar[str] = 'command.result'


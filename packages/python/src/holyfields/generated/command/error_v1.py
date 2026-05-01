from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class CommandErrorV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class CommandErrorV1Payload(BaseModel):
    command_id: str = Field(..., description='ID of the command that failed.')
    target_agent: str = Field(..., description='Agent that attempted the command.')
    action: str = Field(..., description='The command action that failed.')
    error_code: Literal['timeout', 'rejected', 'invalid_state', 'execution_failed', 'not_implemented', 'ttl_expired', 'rate_limited'] = Field(..., description='Machine-readable error classification.')
    error_message: str = Field(..., description='Human-readable error description.')
    retryable: bool = Field(False, description='Whether the command can be retried.')
    retry_after_ms: int | None = Field(None, description='Suggested retry delay in ms. Only meaningful when retryable=true.', ge=0)
    fsm_version: int | None = Field(None, description='FSM version after error transition. Null if error before FSM engagement (e.g., TTL expiry).', ge=1)

class CommandErrorV1(BaseModel):
    """Emitted when a command fails. Contains machine-readable classification and retry guidance."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['command.error'] = Field(..., description='Base event_type. Actual routing: command.{agent}.{action}.error')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: CommandErrorV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: CommandErrorV1Payload

    EVENT_TYPE: ClassVar[str] = 'command.error'


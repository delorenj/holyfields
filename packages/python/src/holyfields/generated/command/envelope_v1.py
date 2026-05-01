from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class CommandEnvelopeV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class CommandEnvelopeV1Payload(BaseModel):
    command_id: str = Field(..., description='Unique ID for this command instance. Used for idempotency, ack/result correlation.')
    target_agent: str = Field(..., description='Agent that should execute this command.')
    issued_by: str = Field(..., description="Identity of the command issuer (agent name, 'system', or human name).", min_length=1)
    action: str = Field(..., description="Command action identifier (e.g., 'run_drift_check', 'assign_ticket').", min_length=1)
    priority: Literal['low', 'normal', 'high', 'critical'] = Field('normal', description="Execution priority. 'critical' bypasses queue ordering.")
    ttl_ms: int = Field(30000, description='Time-to-live in ms. Command rejected if not acked within TTL. 0 = no expiry.', ge=0)
    idempotency_key: str | None = Field(None, description="Optional dedup key. Duplicates within 300s window get outcome='skipped'.")
    command_payload: dict[str, Any] = Field(..., description='Action-specific data. Schema varies by action.')

class CommandEnvelopeV1(BaseModel):
    """Wire-level envelope for commands sent to agents via Bloodbank. Commands are imperative ('do X'), unlike events which are declarative ('X happened')."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['command.envelope'] = Field(..., description='Base event_type for command envelope. Actual routing uses command.{agent}.{action}.')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: CommandEnvelopeV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: CommandEnvelopeV1Payload

    EVENT_TYPE: ClassVar[str] = 'command.envelope'


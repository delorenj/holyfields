from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class CommandEnvelopeV1(BaseModel):
    """Wire-level envelope for commands sent to agents via Bloodbank. Commands are imperative ('do X'), unlike events which are declarative ('X happened')."""

    command_id: str = Field(..., description="Unique ID for this command instance. Used for idempotency, ack/result correlation.")
    target_agent: str = Field(..., description="Agent that should execute this command.")
    issued_by: str = Field(..., description="Identity of the command issuer (agent name, 'system', or human name).", min_length=1)
    action: str = Field(..., description="Command action identifier (e.g., 'run_drift_check', 'assign_ticket').", min_length=1)
    command_payload: dict[str, Any] = Field(..., description="Action-specific data. Schema varies by action.")
    priority: Optional[Literal["low", "normal", "high", "critical"]] = Field(None, description="Execution priority. 'critical' bypasses queue ordering.")
    ttl_ms: Optional[int] = Field(None, description="Time-to-live in ms. Command rejected if not acked within TTL. 0 = no expiry.", ge=0)
    idempotency_key: Optional[str | None] = Field(None, description="Optional dedup key. Duplicates within 300s window get outcome='skipped'.")

    EVENT_TYPE: str = "command.envelope"

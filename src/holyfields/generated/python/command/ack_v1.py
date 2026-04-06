from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class CommandAckV1(BaseModel):
    """Emitted immediately when an agent accepts a command for processing. Indicates the command passed all guards (TTL, idempotency, FSM state)."""

    command_id: str = Field(..., description="ID of the command being acknowledged.")
    target_agent: str = Field(..., description="Agent that accepted the command.")
    action: str = Field(..., description="The command action being acknowledged.")
    fsm_version: int = Field(..., description="FSM version after the acknowledging transition.", ge=1)
    estimated_duration_ms: Optional[int | None] = Field(None, description="Optional estimate of execution time in milliseconds.", ge=0)

    EVENT_TYPE: str = "command.ack"

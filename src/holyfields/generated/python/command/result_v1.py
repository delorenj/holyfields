from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class CommandResultV1(BaseModel):
    """Emitted when an agent completes command execution. Contains outcome classification and optional result data."""

    command_id: str = Field(..., description="ID of the command that produced this result.")
    target_agent: str = Field(..., description="Agent that executed the command.")
    action: str = Field(..., description="The command action that was executed.")
    outcome: str = Field(..., description="'success': completed fully. 'partial': completed with caveats. 'skipped': idempotency dedup, no work done.")
    fsm_version: int = Field(..., description="FSM version after transitioning back to idle.")
    duration_ms: Optional[int | None] = Field(None, description="Execution time from ack to result in milliseconds.")
    result_payload: Optional[dict | None] = Field(None, description="Action-specific result data. Null for skipped outcomes.")

    EVENT_TYPE: str = "command.result"

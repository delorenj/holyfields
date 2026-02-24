from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class CommandErrorV1(BaseModel):
    """Emitted when a command fails. Contains machine-readable classification and retry guidance."""

    command_id: str = Field(..., description="ID of the command that failed.")
    target_agent: str = Field(..., description="Agent that attempted the command.")
    action: str = Field(..., description="The command action that failed.")
    error_code: str = Field(..., description="Machine-readable error classification.")
    error_message: str = Field(..., description="Human-readable error description.")
    retryable: Optional[bool] = Field(None, description="Whether the command can be retried.")
    retry_after_ms: Optional[int | None] = Field(None, description="Suggested retry delay in ms. Only meaningful when retryable=true.")
    fsm_version: Optional[int | None] = Field(None, description="FSM version after error transition. Null if error before FSM engagement (e.g., TTL expiry).")

    EVENT_TYPE: str = "command.error"

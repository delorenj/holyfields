from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentStateChangedV1(BaseModel):
    """Emitted when an agent changes its internal state or thinking process"""

    agent_id: str = Field(..., description="ID of the agent whose state changed")
    state: Literal["idle", "thinking", "working", "error", "paused"] = Field(..., description="Current state")
    thought_process: Optional[str | None] = Field(None, description="Internal monologue or reasoning (optional)")

    EVENT_TYPE: str = "agent.state.changed"

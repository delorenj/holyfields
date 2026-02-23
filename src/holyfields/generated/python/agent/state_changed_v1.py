from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    agent_id: str = Field(..., description="ID of the agent whose state changed")
    state: str = Field(..., description="Current state")
    thought_process: Optional[str | None] = Field(None, description="Internal monologue or reasoning (optional)")


class AgentStateChangedV1(BaseModel):
    """Emitted when an agent changes its internal state or thinking process"""

    event_type: Literal["agent.state.changed"] = "agent.state.changed"
    payload: Payload

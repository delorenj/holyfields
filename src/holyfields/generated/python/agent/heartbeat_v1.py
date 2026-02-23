from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentHeartbeatV1(BaseModel):
    """Periodic agent health signal"""

    agent_name: str = Field(..., description="Name of the agent")
    status: str = Field(..., description="Current agent status")
    active_sessions: Optional[int] = Field(None, description="Number of active sessions")
    uptime_ms: Optional[int] = Field(None, description="Agent uptime in milliseconds")

    EVENT_TYPE: str = "agent.heartbeat"

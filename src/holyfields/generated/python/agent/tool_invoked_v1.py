from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentToolInvokedV1(BaseModel):
    """Agent invoked a tool (exec, web_search, read, etc.)"""

    agent_name: str = Field(..., description="Name of the agent invoking the tool")
    tool_name: str = Field(..., description="Name of the tool (e.g., 'exec', 'web_search', 'read')")
    tool_params_preview: str = Field(..., description="First 200 characters of tool parameters")
    session_key: str = Field(..., description="Session identifier")

    EVENT_TYPE: str = "agent.tool.invoked"

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    session_id: str = Field(..., description="Claude Code session ID")
    thread_id: Optional[str | None] = Field(None, description="Thread ID")
    tool_name: str = Field(..., description="Name of the tool invoked")
    tool_input: Optional[dict[str, Any]] = Field(None, description="Tool input parameters")
    working_directory: Optional[str | None] = Field(None, description="Working directory")
    git_branch: Optional[str | None] = Field(None, description="Current git branch")
    files_in_context: Optional[list[str]] = Field(None, description="Files in context")
    turn_number: Optional[int] = Field(None, description="Turn number")
    model: Optional[str] = Field(None, description="Model being used")


class SessionThreadAgentActionV1(BaseModel):
    """Claude Code tool was invoked"""

    event_type: Literal["session.thread.agent.action"] = "session.thread.agent.action"
    payload: Payload

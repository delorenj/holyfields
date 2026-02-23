from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SessionThreadAgentActionV1(BaseModel):
    """Claude Code tool was invoked"""

    session_id: str
    tool_metadata: dict[str, Any] = Field(..., description="Tool invocation metadata")
    thread_id: Optional[str | None] = None
    tool_name: Optional[str] = Field(None, description="Name of the tool invoked")
    tool_input: Optional[dict[str, Any]] = Field(None, description="Tool input parameters")
    working_directory: Optional[str | None] = None
    git_branch: Optional[str | None] = None
    files_in_context: Optional[list[str]] = None
    turn_number: Optional[int | None] = None
    model: Optional[str | None] = None
    conversation_id: Optional[str | None] = None
    git_status: Optional[str | None] = None
    tags: Optional[list[str]] = None

    EVENT_TYPE: str = "session.thread.agent.action"

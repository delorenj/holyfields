from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    session_id: str = Field(..., description="Claude Code session ID")
    thread_id: Optional[str | None] = Field(None, description="Thread ID if available")
    working_directory: str = Field(..., description="Working directory for the session")
    git_branch: Optional[str | None] = Field(None, description="Git branch if in a repo")
    git_remote: Optional[str | None] = Field(None, description="Git remote URL if available")
    model: str = Field(..., description="Claude model being used")
    user_prompt: Optional[str | None] = Field(None, description="Initial user prompt if available")
    context_files: Optional[list[str]] = Field(None, description="Files in context")
    mcp_servers: Optional[list[str]] = Field(None, description="MCP servers configured")


class SessionThreadStartV1(BaseModel):
    """Claude Code session started"""

    event_type: Literal["session.thread.start"] = "session.thread.start"
    payload: Payload

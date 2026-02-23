from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SessionThreadStartV1(BaseModel):
    """Claude Code session started"""

    session_id: str = Field(..., description="Claude Code session ID")
    working_directory: str = Field(..., description="Working directory for the session")
    model: str = Field(..., description="Claude model being used")
    thread_id: Optional[str | None] = Field(None, description="Thread ID if available")
    git_branch: Optional[str | None] = Field(None, description="Git branch if in a repo")
    git_remote: Optional[str | None] = Field(None, description="Git remote URL if available")
    user_prompt: Optional[str | None] = Field(None, description="Initial user prompt if available")
    context_files: Optional[list[str]] = Field(None, description="Files in context")
    mcp_servers: Optional[list[str]] = Field(None, description="MCP servers configured")

    EVENT_TYPE: str = "session.thread.start"

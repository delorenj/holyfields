from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SessionThreadStartV1(BaseModel):
    """Claude Code session started"""

    session_id: str
    working_directory: str
    model: str
    thread_id: Optional[str | None] = None
    git_branch: Optional[str | None] = None
    git_remote: Optional[str | None] = None
    user_prompt: Optional[str | None] = None
    context_files: Optional[list[str]] = None
    mcp_servers: Optional[list[str]] = None
    started_at: Optional[str] = None

    EVENT_TYPE: str = "session.thread.start"

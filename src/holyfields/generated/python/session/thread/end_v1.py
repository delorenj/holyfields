from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SessionThreadEndV1(BaseModel):
    """Claude Code session ended"""

    session_id: str
    end_reason: str
    final_status: str
    thread_id: Optional[str | None] = None
    duration_seconds: Optional[int | None] = None
    total_turns: Optional[int] = None
    total_tokens: Optional[int | None] = None
    total_cost_usd: Optional[float | None] = None
    tools_used: Optional[int] = None
    files_modified: Optional[list[str]] = None
    git_commits: Optional[list[str]] = None
    summary: Optional[str | None] = None
    working_directory: Optional[str | None] = None
    git_branch: Optional[str | None] = None

    EVENT_TYPE: str = "session.thread.end"

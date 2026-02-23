from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SessionThreadEndV1(BaseModel):
    """Claude Code session ended"""

    session_id: str = Field(..., description="Claude Code session ID")
    end_reason: str = Field(..., description="Reason the session ended")
    total_turns: int = Field(..., description="Total conversation turns")
    final_status: str = Field(..., description="Final session status")
    thread_id: Optional[str | None] = Field(None, description="Thread ID if available")
    duration_seconds: Optional[int] = Field(None, description="Session duration in seconds")
    total_tokens: Optional[int] = Field(None, description="Total tokens consumed")
    total_cost_usd: Optional[float] = Field(None, description="Total cost in USD")
    tools_used: Optional[dict[str, Any]] = Field(None, description="Map of tool name to invocation count")
    files_modified: Optional[list[str]] = Field(None, description="Files that were modified")
    git_commits: Optional[list[str]] = Field(None, description="Commit SHAs created")
    summary: Optional[str | None] = Field(None, description="Session summary if generated")

    EVENT_TYPE: str = "session.thread.end"

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    session_id: str = Field(..., description="Claude Code session ID")
    thread_id: Optional[str | None] = Field(None, description="Thread ID if available")
    end_reason: str = Field(..., description="Reason the session ended")
    duration_seconds: Optional[int] = Field(None, description="Session duration in seconds")
    total_turns: int = Field(..., description="Total conversation turns")
    total_tokens: Optional[int] = Field(None, description="Total tokens consumed")
    total_cost_usd: Optional[float] = Field(None, description="Total cost in USD")
    tools_used: Optional[dict[str, Any]] = Field(None, description="Map of tool name to invocation count")
    files_modified: Optional[list[str]] = Field(None, description="Files that were modified")
    git_commits: Optional[list[str]] = Field(None, description="Commit SHAs created")
    final_status: str = Field(..., description="Final session status")
    summary: Optional[str | None] = Field(None, description="Session summary if generated")


class SessionThreadEndV1(BaseModel):
    """Claude Code session ended"""

    event_type: Literal["session.thread.end"] = "session.thread.end"
    payload: Payload

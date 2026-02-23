from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SessionThreadErrorV1(BaseModel):
    """Error occurred during session"""

    session_id: str = Field(..., description="Claude Code session ID")
    error_type: str = Field(..., description="Type of error")
    error_message: str = Field(..., description="Error message")
    thread_id: Optional[str | None] = Field(None, description="Thread ID")
    stack_trace: Optional[str | None] = Field(None, description="Stack trace if available")
    tool_name: Optional[str | None] = Field(None, description="Tool that caused error")
    recoverable: Optional[bool] = Field(None, description="Whether error is recoverable")
    turn_number: Optional[int | None] = Field(None, description="Turn number when error occurred")

    EVENT_TYPE: str = "session.thread.error"

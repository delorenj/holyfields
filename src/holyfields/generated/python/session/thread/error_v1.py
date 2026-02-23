from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    session_id: str = Field(..., description="Claude Code session ID")
    thread_id: Optional[str | None] = Field(None, description="Thread ID")
    error_type: str = Field(..., description="Type of error")
    error_message: str = Field(..., description="Error message")
    stack_trace: Optional[str | None] = Field(None, description="Stack trace if available")
    tool_name: Optional[str | None] = Field(None, description="Tool that caused error")
    recoverable: Optional[bool] = Field(None, description="Whether error is recoverable")
    turn_number: Optional[int | None] = Field(None, description="Turn number when error occurred")


class SessionThreadErrorV1(BaseModel):
    """Error occurred during session"""

    event_type: Literal["session.thread.error"] = "session.thread.error"
    payload: Payload

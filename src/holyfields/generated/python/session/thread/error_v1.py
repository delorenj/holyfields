from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SessionThreadErrorV1(BaseModel):
    """Error occurred during session"""

    session_id: str
    error_type: str
    error_message: str
    thread_id: Optional[str | None] = None
    stack_trace: Optional[str | None] = None
    tool_name: Optional[str | None] = None
    recoverable: Optional[bool] = None
    turn_number: Optional[int | None] = None

    EVENT_TYPE: str = "session.thread.error"

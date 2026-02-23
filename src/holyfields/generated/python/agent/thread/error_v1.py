from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentThreadErrorV1(BaseModel):
    """Agent interaction failed"""

    provider: str
    error_message: str
    model: Optional[str | None] = None
    error_code: Optional[str | None] = None
    is_retryable: Optional[bool] = None
    retry_count: Optional[int] = None

    EVENT_TYPE: str = "agent.thread.error"

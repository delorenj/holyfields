from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentThreadResponseV1(BaseModel):
    """Agent responded to prompt"""

    provider: str
    response: str
    prompt_id: Optional[str | None] = Field(None, description="Deprecated - use correlation_ids")
    model: Optional[str | None] = None
    tokens_used: Optional[int | None] = None
    duration_ms: Optional[int | None] = None

    EVENT_TYPE: str = "agent.thread.response"

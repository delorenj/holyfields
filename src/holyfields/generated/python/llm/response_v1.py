from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class LlmResponseV1(BaseModel):
    """[DEPRECATED] Use agent.thread.response instead. LLM responded to prompt."""

    provider: str = Field(..., description="LLM provider")
    response: str = Field(..., description="Response text")
    model: Optional[str | None] = Field(None, description="Model used")
    tokens_used: Optional[int | None] = Field(None, description="Tokens consumed", ge=0)
    duration_ms: Optional[int | None] = Field(None, description="Response time", ge=0)
    deprecated: Optional[str] = Field(None, alias="_deprecated", description="Deprecation notice")

    EVENT_TYPE: str = "llm.response"

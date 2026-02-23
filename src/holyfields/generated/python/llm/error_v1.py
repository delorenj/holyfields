from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    provider: str = Field(..., description="LLM provider")
    error_message: str = Field(..., description="Error message")
    model: Optional[str | None] = Field(None, description="Model being used")
    error_code: Optional[str | None] = Field(None, description="Error code")
    is_retryable: Optional[bool] = Field(None, description="Whether error is retryable")
    retry_count: Optional[int] = Field(None, description="Retry attempts")
    deprecated: Optional[str] = Field(None, alias="_deprecated", description="Deprecation notice")


class LlmErrorV1(BaseModel):
    """[DEPRECATED] Use agent.thread.error instead. LLM interaction failed."""

    event_type: Literal["llm.error"] = "llm.error"
    payload: Payload

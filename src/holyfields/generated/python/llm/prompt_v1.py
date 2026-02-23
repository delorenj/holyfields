from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    provider: str = Field(..., description="LLM provider")
    model: Optional[str | None] = Field(None, description="Model name")
    prompt: str = Field(..., description="Prompt text")
    project: Optional[str | None] = Field(None, description="Git project name")
    tags: Optional[list[str]] = Field(None, description="Tags")
    deprecated: Optional[str] = Field(None, alias="_deprecated", description="Deprecation notice")


class LlmPromptV1(BaseModel):
    """[DEPRECATED] Use agent.thread.prompt instead. LLM interaction started."""

    event_type: Literal["llm.prompt"] = "llm.prompt"
    payload: Payload

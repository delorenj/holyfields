from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class LlmPromptV1(BaseModel):
    """[DEPRECATED] Use agent.thread.prompt instead. LLM interaction started."""

    provider: str = Field(..., description="LLM provider")
    prompt: str = Field(..., description="Prompt text")
    model: Optional[str | None] = Field(None, description="Model name")
    project: Optional[str | None] = Field(None, description="Git project name")
    tags: Optional[list[str]] = Field(None, description="Tags")
    deprecated: Optional[str] = Field(None, alias="_deprecated", description="Deprecation notice")

    EVENT_TYPE: str = "llm.prompt"

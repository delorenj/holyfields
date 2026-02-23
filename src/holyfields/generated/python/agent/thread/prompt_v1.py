from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentThreadPromptV1(BaseModel):
    """A prompt is sent to an agent thread"""

    provider: str
    prompt: str
    model: Optional[str | None] = None
    project: Optional[str | None] = None
    working_dir: Optional[str | None] = None
    domain: Optional[str | None] = None
    tags: Optional[list[str]] = None

    EVENT_TYPE: str = "agent.thread.prompt"

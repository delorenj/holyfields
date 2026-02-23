from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentThreadPromptV1(BaseModel):
    """A prompt is sent to an agent thread"""

    agent_name: str = Field(..., description="Name of the agent receiving the prompt")
    provider: str = Field(..., description="LLM provider (e.g., 'anthropic', 'openai', 'google')")
    prompt: str = Field(..., description="The prompt text")
    model: Optional[str] = Field(None, description="Specific model used")
    project: Optional[str | None] = Field(None, description="Git project name if applicable")
    working_dir: Optional[str | None] = Field(None, description="Working directory for the session")
    tags: Optional[list[str]] = Field(None, description="Tags for categorizing this prompt")

    EVENT_TYPE: str = "agent.thread.prompt"

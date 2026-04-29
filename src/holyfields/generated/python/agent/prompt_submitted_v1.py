from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentPromptSubmittedV1(BaseModel):
    """Emitted when a user submits a prompt to an agent. Producer is the agent runtime (e.g. Claude Code via .claude/hooks/bloodbank-publisher.sh on UserPromptSubmit). Carries the raw prompt text alongside repo state at submission time. Consumers use it to attribute downstream tool invocations to a user intent and to build retrospective views of what was asked."""

    pass

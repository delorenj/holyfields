from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentToolRequestedV1(BaseModel):
    """Emitted before an agent invokes a tool. Pairs with agent.tool.invoked: the request fires from the PreToolUse hook (intent), the invocation fires from the PostToolUse hook (result). Same session_id correlates them. Consumers use the pairing to detect tools that requested but never completed (cancellation, timeout, agent crash)."""

    pass

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentToolInvokedV1(BaseModel):
    """Emitted when an agent invokes a tool. One event per invocation. Carries enough context (tool name, raw input, session, repo state) for downstream observability without persisting full conversation history. The tool_input field is opaque on purpose: each tool defines its own input shape and this schema does not constrain it."""

    pass

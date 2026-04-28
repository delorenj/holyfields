from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentSessionStartedV1(BaseModel):
    """Emitted when an agent session begins. Producer is typically the agent runtime itself (e.g., Claude Code via .claude/hooks/bloodbank-publisher.sh on SessionStart). Consumers track session lifecycle, attribute downstream events to a session, and aggregate per-session metrics."""

    pass

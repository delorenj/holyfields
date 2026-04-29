from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentSubagentCompletedV1(BaseModel):
    """Emitted when a subagent (a Task-tool spawned helper) finishes. Producer is the agent runtime (e.g. Claude Code via .claude/hooks/bloodbank-publisher.sh on SubagentStop). Distinct from agent.session.ended: the parent session continues; only the subagent has terminated. The session_id field points to the PARENT session so subagent activity rolls up under the originating session."""

    pass

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentSessionEndedV1(BaseModel):
    """Emitted when an agent session terminates. Carries summary statistics of the session (turn count, tool histogram, files touched, commits created) so consumers can build retrospective views without replaying every agent.tool.invoked event."""

    pass

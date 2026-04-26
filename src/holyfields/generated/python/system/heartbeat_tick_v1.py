from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SystemHeartbeatTickV1(BaseModel):
    """Periodic heartbeat event emitted by a tick service. Consumers use it for liveness monitoring, scheduled task fan-out, restart detection, and as a synthetic load source for testing the v3 event platform. The first real-world domain event in the v3 ecosystem; pattern reference for future domain events."""

    pass

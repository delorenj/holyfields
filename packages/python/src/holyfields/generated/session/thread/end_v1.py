from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class SessionThreadEndV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class SessionThreadEndV1Payload(BaseModel):
    session_id: str
    thread_id: str | None = None
    end_reason: str
    duration_seconds: int | None = None
    total_turns: int | None = None
    total_tokens: int | None = None
    total_cost_usd: float | None = None
    tools_used: int | None = None
    files_modified: list[str] | None = None
    git_commits: list[str] | None = None
    final_status: str
    summary: str | None = None
    working_directory: str | None = None
    git_branch: str | None = None

class SessionThreadEndV1(BaseModel):
    """Claude Code session ended"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['session.thread.end'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: SessionThreadEndV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: SessionThreadEndV1Payload

    EVENT_TYPE: ClassVar[str] = 'session.thread.end'


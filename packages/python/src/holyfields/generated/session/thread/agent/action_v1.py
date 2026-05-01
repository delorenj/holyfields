from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class SessionThreadAgentActionV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class SessionThreadAgentActionV1Payload(BaseModel):
    session_id: str
    thread_id: str | None = None
    tool_name: str | None = Field(None, description='Name of the tool invoked')
    tool_input: dict[str, Any] | None = Field(None, description='Tool input parameters')
    working_directory: str | None = None
    git_branch: str | None = None
    files_in_context: list[str] | None = None
    turn_number: int | None = None
    model: str | None = None
    conversation_id: str | None = None
    tool_metadata: dict[str, Any] = Field(..., description='Tool invocation metadata')
    git_status: str | None = None
    tags: list[str] | None = None

class SessionThreadAgentActionV1(BaseModel):
    """Claude Code tool was invoked"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['session.thread.agent.action'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: SessionThreadAgentActionV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: SessionThreadAgentActionV1Payload

    EVENT_TYPE: ClassVar[str] = 'session.thread.agent.action'


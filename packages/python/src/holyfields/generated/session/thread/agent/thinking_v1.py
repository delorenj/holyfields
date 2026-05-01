from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class SessionThreadAgentThinkingV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class SessionThreadAgentThinkingV1Payload(BaseModel):
    session_id: str
    thread_id: str | None = None
    thinking_text: str
    thinking_duration_ms: int | None = None
    turn_number: int | None = None
    triggered_by_tool: str | None = None

class SessionThreadAgentThinkingV1(BaseModel):
    """Claude Code thinking/reasoning event"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['session.thread.agent.thinking'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: SessionThreadAgentThinkingV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: SessionThreadAgentThinkingV1Payload

    EVENT_TYPE: ClassVar[str] = 'session.thread.agent.thinking'


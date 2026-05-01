from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentFeedbackResponseV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentFeedbackResponseV1Payload(BaseModel):
    agent_id: str = Field(..., description='AgentForge registry ID')
    letta_agent_id: str | None = Field(None, description='Letta agent ID if different')
    response: str = Field(..., description="Agent's response text")
    status: Literal['ok', 'error'] = Field(..., description='Response status')
    error_message: str | None = Field(None, description='Error message if status is error')
    metadata: dict[str, Any] | None = Field(None, description='Additional metadata')

class AgentFeedbackResponseV1(BaseModel):
    """Agent feedback response"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.feedback.response'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentFeedbackResponseV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentFeedbackResponseV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.feedback.response'


from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentMessageSentV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentMessageSentV1Payload(BaseModel):
    agent_name: str = Field(..., description='Name of the agent that sent the message')
    channel: str = Field(..., description='Channel the message was sent to')
    message_preview: str = Field(..., description='First 200 characters of the response', max_length=200)
    message_length: int = Field(..., description='Total length of the response in characters', ge=0)
    model: str | None = Field(None, description='AI model used to generate the response')
    tokens_used: int | None = Field(None, description='Total tokens consumed (input + output)', ge=0)
    duration_ms: int | None = Field(None, description='Time to generate response in milliseconds', ge=0)

class AgentMessageSentV1(BaseModel):
    """Outbound response sent by an agent"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.message.sent'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentMessageSentV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentMessageSentV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.message.sent'


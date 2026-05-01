from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class LlmResponseV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class LlmResponseV1Payload(BaseModel):
    provider: str = Field(..., description='LLM provider')
    response: str = Field(..., description='Response text')
    model: str | None = Field(None, description='Model used')
    tokens_used: int | None = Field(None, description='Tokens consumed', ge=0)
    duration_ms: int | None = Field(None, description='Response time', ge=0)
    deprecated: Literal['Use agent.thread.response instead'] | None = Field(None, alias='_deprecated', description='Deprecation notice')

class LlmResponseV1(BaseModel):
    """[DEPRECATED] Use agent.thread.response instead. LLM responded to prompt."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['llm.response'] = Field(..., description='Event type discriminator - DEPRECATED')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: LlmResponseV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: LlmResponseV1Payload

    EVENT_TYPE: ClassVar[str] = 'llm.response'


from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class LlmErrorV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class LlmErrorV1Payload(BaseModel):
    provider: str = Field(..., description='LLM provider')
    error_message: str = Field(..., description='Error message')
    model: str | None = Field(None, description='Model being used')
    error_code: str | None = Field(None, description='Error code')
    is_retryable: bool | None = Field(None, description='Whether error is retryable')
    retry_count: int | None = Field(None, description='Retry attempts', ge=0)
    deprecated: Literal['Use agent.thread.error instead'] | None = Field(None, alias='_deprecated', description='Deprecation notice')

class LlmErrorV1(BaseModel):
    """[DEPRECATED] Use agent.thread.error instead. LLM interaction failed."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['llm.error'] = Field(..., description='Event type discriminator - DEPRECATED')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: LlmErrorV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: LlmErrorV1Payload

    EVENT_TYPE: ClassVar[str] = 'llm.error'


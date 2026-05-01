from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class LlmPromptV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class LlmPromptV1Payload(BaseModel):
    provider: str = Field(..., description='LLM provider')
    model: str | None = Field(None, description='Model name')
    prompt: str = Field(..., description='Prompt text')
    project: str | None = Field(None, description='Git project name')
    tags: list[str] | None = Field(None, description='Tags')
    deprecated: Literal['Use agent.thread.prompt instead'] | None = Field(None, alias='_deprecated', description='Deprecation notice')

class LlmPromptV1(BaseModel):
    """[DEPRECATED] Use agent.thread.prompt instead. LLM interaction started."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['llm.prompt'] = Field(..., description='Event type discriminator - DEPRECATED')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: LlmPromptV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: LlmPromptV1Payload

    EVENT_TYPE: ClassVar[str] = 'llm.prompt'


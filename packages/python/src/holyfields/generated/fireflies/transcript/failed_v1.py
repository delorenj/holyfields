from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class FirefliesTranscriptFailedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class FirefliesTranscriptFailedV1Payload(BaseModel):
    failed_stage: Literal['upload', 'transcription', 'processing'] = Field(..., description='Stage that failed')
    error_message: str = Field(..., description='Error message')
    error_code: str | None = Field(None, description='Error code')
    transcript_id: str | None = Field(None, description='Transcript ID if available')
    media_file: str | None = Field(None, description='Original file path')
    retry_count: int | None = Field(None, description='Retry attempts', ge=0)
    is_retryable: bool | None = Field(None, description='Whether error is retryable')

class FirefliesTranscriptFailedV1(BaseModel):
    """Transcription or processing failed"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['fireflies.transcript.failed'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: FirefliesTranscriptFailedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: FirefliesTranscriptFailedV1Payload

    EVENT_TYPE: ClassVar[str] = 'fireflies.transcript.failed'


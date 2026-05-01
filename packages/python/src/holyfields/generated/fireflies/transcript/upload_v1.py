from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class FirefliesTranscriptUploadV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class FirefliesTranscriptUploadV1Payload(BaseModel):
    media_file: str = Field(..., description='Path or URL to media file')
    media_duration_seconds: int = Field(..., description='Duration of media in seconds', ge=1)
    media_type: str = Field(..., description="MIME type (e.g., 'audio/mpeg', 'video/mp4')")
    title: str | None = Field(None, description='Meeting title')
    user_id: str | None = Field(None, description='User requesting transcription')
    content_hash: str | None = Field(None, description='SHA256 hash of source audio file for deduplication')

class FirefliesTranscriptUploadV1(BaseModel):
    """Request to upload media to Fireflies for transcription"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['fireflies.transcript.upload'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: FirefliesTranscriptUploadV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: FirefliesTranscriptUploadV1Payload

    EVENT_TYPE: ClassVar[str] = 'fireflies.transcript.upload'


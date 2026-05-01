from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class ArtifactAudioDetectedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class ArtifactAudioDetectedV1Payload(BaseModel):
    inbox_source: Literal['audio inbox'] = Field(..., description='Human-readable logical source where file was detected')
    file_name: str = Field(..., description='Detected file name', min_length=1)
    file_path: str = Field(..., description='Absolute or relative file path as seen by the detector', min_length=1)
    file_extension: str = Field(..., description="Lowercase extension without dot (e.g. 'mp3', 'wav', 'm4a', 'ogg')", pattern='^[a-z0-9]+$')
    mime_type: str | None = Field(None, description='Detected MIME type if known')
    file_size_bytes: int | None = Field(None, description='File size in bytes if known', ge=0)
    detected_at: str = Field(..., description='Timestamp when detector noticed the file')
    detector: str | None = Field(None, description="Detector identity (e.g. 'node-red-flow-orchestrator')")
    sha256: str | None = Field(None, description='Optional content hash for dedupe/correlation', pattern='^[a-f0-9]{64}$')
    metadata: dict[str, Any] | None = Field(None, description='Additional source-specific metadata')

class ArtifactAudioDetectedV1(BaseModel):
    """Audio file detected in the audio inbox and ready for downstream workflow processing"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['artifact.audio.detected'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: ArtifactAudioDetectedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: ArtifactAudioDetectedV1Payload

    EVENT_TYPE: ClassVar[str] = 'artifact.audio.detected'


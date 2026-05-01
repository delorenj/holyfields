from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class ArtifactIngestionFailedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class ArtifactIngestionFailedV1Payload(BaseModel):
    artifact_uri: str = Field(..., description='URI of the artifact that failed ingestion')
    artifact_kind: str = Field(..., description='Type of artifact')
    error_message: str = Field(..., description='Error message')
    error_code: str | None = Field(None, description='Error code if available')
    retry_count: int | None = Field(None, description='Number of retry attempts', ge=0)
    is_retryable: bool | None = Field(None, description='Whether the error is retryable')

class ArtifactIngestionFailedV1(BaseModel):
    """Artifact ingestion into RAG failed"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['artifact.ingestion.failed'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: ArtifactIngestionFailedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: ArtifactIngestionFailedV1Payload

    EVENT_TYPE: ClassVar[str] = 'artifact.ingestion.failed'


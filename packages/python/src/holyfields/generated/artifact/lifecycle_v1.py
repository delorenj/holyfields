from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class ArtifactLifecycleV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class ArtifactLifecycleV1Payload(BaseModel):
    action: Literal['created', 'updated', 'deleted'] = Field(..., description='Lifecycle action')
    kind: Literal['transcript', 'code', 'document', 'image', 'audio'] = Field(..., description='Type of artifact')
    uri: str = Field(..., description='File path or URL')
    title: str | None = Field(None, description='Artifact title')
    content: str | None = Field(None, description='Full content if applicable')
    metadata: dict[str, Any] | None = Field(None, description='Additional metadata')

class ArtifactLifecycleV1(BaseModel):
    """Artifact was created, updated, or deleted"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['artifact.created', 'artifact.updated', 'artifact.deleted'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: ArtifactLifecycleV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: ArtifactLifecycleV1Payload


from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class FirefliesTranscriptProcessedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class FirefliesTranscriptProcessedV1Payload(BaseModel):
    transcript_id: str = Field(..., description='Fireflies transcript ID')
    rag_document_id: str = Field(..., description='Internal RAG document ID')
    title: str = Field(..., description='Meeting title')
    sentence_count: int | None = Field(None, description='Number of sentences ingested', ge=0)
    speaker_count: int | None = Field(None, description='Number of unique speakers', ge=1)
    duration_minutes: float | None = Field(None, description='Duration in minutes', ge=0)
    vector_store: str = Field(..., description="Vector store used (e.g., 'chroma', 'pinecone')")
    chunk_count: int | None = Field(None, description='Number of chunks created', ge=0)
    embedding_model: str | None = Field(None, description='Model used for embeddings')

class FirefliesTranscriptProcessedV1(BaseModel):
    """Transcript was ingested into RAG system"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['fireflies.transcript.processed'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: FirefliesTranscriptProcessedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: FirefliesTranscriptProcessedV1Payload

    EVENT_TYPE: ClassVar[str] = 'fireflies.transcript.processed'


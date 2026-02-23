from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    transcript_id: str = Field(..., description="Fireflies transcript ID")
    rag_document_id: str = Field(..., description="Internal RAG document ID")
    title: str = Field(..., description="Meeting title")
    sentence_count: Optional[int] = Field(None, description="Number of sentences ingested")
    speaker_count: Optional[int] = Field(None, description="Number of unique speakers")
    duration_minutes: Optional[float] = Field(None, description="Duration in minutes")
    vector_store: str = Field(..., description="Vector store used (e.g., 'chroma', 'pinecone')")
    chunk_count: Optional[int] = Field(None, description="Number of chunks created")
    embedding_model: Optional[str | None] = Field(None, description="Model used for embeddings")


class FirefliesTranscriptProcessedV1(BaseModel):
    """Transcript was ingested into RAG system"""

    event_type: Literal["fireflies.transcript.processed"] = "fireflies.transcript.processed"
    payload: Payload

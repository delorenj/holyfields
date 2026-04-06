from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class FirefliesTranscriptProcessedV1(BaseModel):
    """Transcript was ingested into RAG system"""

    transcript_id: str = Field(..., description="Fireflies transcript ID")
    rag_document_id: str = Field(..., description="Internal RAG document ID")
    title: str = Field(..., description="Meeting title")
    vector_store: str = Field(..., description="Vector store used (e.g., 'chroma', 'pinecone')")
    sentence_count: Optional[int] = Field(None, description="Number of sentences ingested", ge=0)
    speaker_count: Optional[int] = Field(None, description="Number of unique speakers", ge=1)
    duration_minutes: Optional[float] = Field(None, description="Duration in minutes", ge=0)
    chunk_count: Optional[int] = Field(None, description="Number of chunks created", ge=0)
    embedding_model: Optional[str | None] = Field(None, description="Model used for embeddings")

    EVENT_TYPE: str = "fireflies.transcript.processed"

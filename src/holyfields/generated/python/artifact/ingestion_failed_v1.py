from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class ArtifactIngestionFailedV1(BaseModel):
    """Artifact ingestion into RAG failed"""

    artifact_uri: str = Field(..., description="URI of the artifact that failed ingestion")
    artifact_kind: str = Field(..., description="Type of artifact")
    error_message: str = Field(..., description="Error message")
    error_code: Optional[str | None] = Field(None, description="Error code if available")
    retry_count: Optional[int] = Field(None, description="Number of retry attempts", ge=0)
    is_retryable: Optional[bool] = Field(None, description="Whether the error is retryable")

    EVENT_TYPE: str = "artifact.ingestion.failed"

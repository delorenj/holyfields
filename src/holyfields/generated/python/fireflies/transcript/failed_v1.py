from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class FirefliesTranscriptFailedV1(BaseModel):
    """Transcription or processing failed"""

    failed_stage: Literal["upload", "transcription", "processing"] = Field(..., description="Stage that failed")
    error_message: str = Field(..., description="Error message")
    error_code: Optional[str | None] = Field(None, description="Error code")
    transcript_id: Optional[str | None] = Field(None, description="Transcript ID if available")
    media_file: Optional[str | None] = Field(None, description="Original file path")
    retry_count: Optional[int] = Field(None, description="Retry attempts", ge=0)
    is_retryable: Optional[bool] = Field(None, description="Whether error is retryable")

    EVENT_TYPE: str = "fireflies.transcript.failed"

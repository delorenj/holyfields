from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    failed_stage: str = Field(..., description="Stage that failed")
    error_message: str = Field(..., description="Error message")
    error_code: Optional[str | None] = Field(None, description="Error code")
    transcript_id: Optional[str | None] = Field(None, description="Transcript ID if available")
    media_file: Optional[str | None] = Field(None, description="Original file path")
    retry_count: Optional[int] = Field(None, description="Retry attempts")
    is_retryable: Optional[bool] = Field(None, description="Whether error is retryable")


class FirefliesTranscriptFailedV1(BaseModel):
    """Transcription or processing failed"""

    event_type: Literal["fireflies.transcript.failed"] = "fireflies.transcript.failed"
    payload: Payload

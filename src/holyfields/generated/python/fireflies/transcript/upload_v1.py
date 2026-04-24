from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class FirefliesTranscriptUploadV1(BaseModel):
    """Request to upload media to Fireflies for transcription"""

    media_file: str = Field(..., description="Path or URL to media file")
    media_duration_seconds: int = Field(..., description="Duration of media in seconds", ge=1)
    media_type: str = Field(..., description="MIME type (e.g., 'audio/mpeg', 'video/mp4')")
    title: Optional[str | None] = Field(None, description="Meeting title")
    user_id: Optional[str | None] = Field(None, description="User requesting transcription")
    content_hash: Optional[str | None] = Field(None, description="SHA256 hash of source audio file for deduplication")

    EVENT_TYPE: str = "fireflies.transcript.upload"

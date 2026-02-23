from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    media_file: str = Field(..., description="Path or URL to media file")
    media_duration_seconds: int = Field(..., description="Duration of media in seconds")
    media_type: str = Field(..., description="MIME type (e.g., 'audio/mpeg', 'video/mp4')")
    title: Optional[str | None] = Field(None, description="Meeting title")
    user_id: Optional[str | None] = Field(None, description="User requesting transcription")


class FirefliesTranscriptUploadV1(BaseModel):
    """Request to upload media to Fireflies for transcription"""

    event_type: Literal["fireflies.transcript.upload"] = "fireflies.transcript.upload"
    payload: Payload

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    transcript_id: str = Field(..., description="Fireflies meeting/transcript ID")
    title: str = Field(..., description="Meeting title")
    date: str = Field(..., description="Meeting date/time")
    duration_minutes: float = Field(..., description="Duration in minutes")
    transcript_url: str = Field(..., description="URL to transcript")
    audio_url: Optional[str | None] = Field(None, description="URL to audio if available")
    video_url: Optional[str | None] = Field(None, description="URL to video if available")
    sentences: list[Any] = Field(..., description="Transcript sentences")
    summary: Optional[str | None] = Field(None, description="Meeting summary if generated")
    participants: Optional[list[dict[str, Any]]] = None


class FirefliesTranscriptReadyV1(BaseModel):
    """Fireflies completed transcription"""

    event_type: Literal["fireflies.transcript.ready"] = "fireflies.transcript.ready"
    payload: Payload

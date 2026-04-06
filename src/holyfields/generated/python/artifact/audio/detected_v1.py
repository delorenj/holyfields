from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class ArtifactAudioDetectedV1(BaseModel):
    """Audio file detected in the audio inbox and ready for downstream workflow processing"""

    inbox_source: str = Field(..., description="Human-readable logical source where file was detected")
    file_name: str = Field(..., description="Detected file name", min_length=1)
    file_path: str = Field(..., description="Absolute or relative file path as seen by the detector", min_length=1)
    file_extension: str = Field(..., description="Lowercase extension without dot (e.g. 'mp3', 'wav', 'm4a', 'ogg')")
    detected_at: str = Field(..., description="Timestamp when detector noticed the file")
    mime_type: Optional[str | None] = Field(None, description="Detected MIME type if known")
    file_size_bytes: Optional[int | None] = Field(None, description="File size in bytes if known", ge=0)
    detector: Optional[str | None] = Field(None, description="Detector identity (e.g. 'node-red-flow-orchestrator')")
    sha256: Optional[str | None] = Field(None, description="Optional content hash for dedupe/correlation")
    metadata: Optional[dict[str, Any]] = Field(None, description="Additional source-specific metadata")

    EVENT_TYPE: str = "artifact.audio.detected"

#!/usr/bin/env python3
"""Generate Python Pydantic bindings for voice transcription schema."""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime


def generate_pydantic_model(schema_path: Path, output_path: Path) -> None:
    """Generate Pydantic model from JSON schema."""

    with open(schema_path) as f:
        schema = json.load(f)

    model_code = '''"""Voice Transcription Event Model.

DO NOT EDIT MANUALLY. Generated from JSON Schema.
Schema: voice/transcription.v1.schema.json
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, constr, confloat, conint


class TranscriptionSource(str, Enum):
    """Valid transcription sources."""
    WHISPERLIVEKIT = "whisperlivekit"
    MOBILE_CLIENT = "mobile-client"
    DESKTOP_CLIENT = "desktop-client"
    CHROME_EXTENSION = "chrome-extension"


class WhisperModel(str, Enum):
    """Valid Whisper model names."""
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE_V2 = "large-v2"
    LARGE_V3 = "large-v3"


class DeviceType(str, Enum):
    """Valid device types."""
    MOBILE = "mobile"
    DESKTOP = "desktop"
    BROWSER = "browser"


class AudioMetadata(BaseModel):
    """Audio metadata for transcription."""
    duration_seconds: Optional[confloat(ge=0)] = Field(
        None, description="Duration of the audio segment in seconds"
    )
    sample_rate: Optional[conint(ge=8000)] = Field(
        None, description="Audio sample rate in Hz"
    )
    confidence: Optional[confloat(ge=0, le=1)] = Field(
        None, description="Transcription confidence score (0-1)"
    )
    language: Optional[str] = Field(
        None,
        description="Detected or specified language code (ISO 639-1)",
        pattern=r"^[a-z]{2}(-[A-Z]{2})?$"
    )
    model: Optional[WhisperModel] = Field(
        None, description="Whisper model used for transcription"
    )
    speaker_id: Optional[str] = Field(
        None, description="Speaker identifier if diarization is enabled"
    )


class TranscriptionContext(BaseModel):
    """Additional contextual information for transcription."""
    device_type: Optional[DeviceType] = Field(
        None, description="Type of device that initiated the transcription"
    )
    user_id: Optional[str] = Field(
        None, description="Optional user identifier"
    )
    tags: Optional[list[str]] = Field(
        None, description="Optional tags for categorization"
    )


class VoiceTranscriptionEvent(BaseModel):
    """Voice transcription completed event payload.

    Event emitted when voice transcription is completed by WhisperLiveKit.
    Event type: transcription.voice.completed
    """

    text: constr(min_length=1) = Field(
        ..., description="The transcribed text from speech-to-text processing"
    )
    timestamp: datetime = Field(
        ..., description="ISO 8601 timestamp when transcription was completed"
    )
    source: TranscriptionSource = Field(
        ..., description="Source service that produced the transcription"
    )
    target: Optional[str] = Field(
        None,
        description="Target service or consumer for this transcription",
        examples=["tonny", "candybar", "clipboard-agent"]
    )
    session_id: UUID = Field(
        ..., description="Unique session identifier for the WebSocket connection"
    )
    audio_metadata: Optional[AudioMetadata] = Field(
        None, description="Metadata about the audio that was transcribed"
    )
    context: Optional[TranscriptionContext] = Field(
        None, description="Additional contextual information"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "text": "Log this idea: we need better cooling for the rack.",
                    "timestamp": "2026-01-27T10:00:00Z",
                    "source": "whisperlivekit",
                    "target": "tonny",
                    "session_id": "550e8400-e29b-41d4-a716-446655440000",
                    "audio_metadata": {
                        "duration_seconds": 3.5,
                        "sample_rate": 16000,
                        "confidence": 0.95,
                        "language": "en",
                        "model": "base"
                    }
                }
            ]
        }

    @classmethod
    def get_routing_key(cls) -> str:
        """Get the RabbitMQ routing key for this event."""
        return "transcription.voice.completed"
'''

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(model_code)

    print(f"Generated Pydantic model: {output_path}")


if __name__ == "__main__":
    schema_path = Path(__file__).parent.parent / "docs/schemas/voice/transcription.v1.schema.json"
    output_path = Path(__file__).parent.parent / "generated/python/voice_transcription.py"

    generate_pydantic_model(schema_path, output_path)

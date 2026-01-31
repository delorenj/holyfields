"""WhisperLiveKit event schemas.

DO NOT EDIT MANUALLY. Generated from JSON Schemas.
Source: ~/code/33GOD/holyfields/trunk-main/whisperlivekit/events/*.json

To regenerate: mise run generate:python
"""

from .transcription_completed import (
    AudioMetadata,
    BaseVoiceEvent,
    BitDepth,
    Format,
    TranscriptionCompletedEvent,
)

__all__ = [
    "BaseVoiceEvent",
    "AudioMetadata",
    "BitDepth",
    "Format",
    "TranscriptionCompletedEvent",
]

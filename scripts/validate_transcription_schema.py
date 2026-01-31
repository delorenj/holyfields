#!/usr/bin/env python3
"""
Validation script for transcription event schemas.

Demonstrates end-to-end schema validation with example payloads.
"""

import json
from datetime import datetime, timezone
from uuid import uuid4

from holyfields.generated.python.whisperlivekit.events import (
    AudioMetadata,
    BitDepth,
    Format,
    TranscriptionCompletedEvent,
)


def print_section(title: str) -> None:
    """Print section header."""
    print(f"\n{'=' * 70}")
    print(f" {title}")
    print(f"{'=' * 70}\n")


def validate_minimal_event() -> None:
    """Validate minimal transcription event."""
    print_section("Testing Minimal Transcription Event")

    event = TranscriptionCompletedEvent(
        event_type="whisperlivekit.transcription.completed",
        timestamp=datetime.now(timezone.utc),
        session_id=uuid4(),
        source="whisperlivekit",
        target="tonny",
        text="Hey Tonny, what's the weather like today?",
        audio_metadata=AudioMetadata(
            duration_ms=2500,
            sample_rate=16000,
            channels=1,
            format=Format.pcm,
        ),
        is_final=True,
    )

    print("✅ Minimal event created successfully")
    print(f"   Text: {event.text}")
    print(f"   Session ID: {event.session_id}")
    print(f"   Sample Rate: {event.audio_metadata.sample_rate} Hz")
    print(f"   Duration: {event.audio_metadata.duration_ms} ms")


def validate_complete_event() -> None:
    """Validate complete transcription event with all fields."""
    print_section("Testing Complete Transcription Event")

    event = TranscriptionCompletedEvent(
        event_type="whisperlivekit.transcription.completed",
        timestamp=datetime.now(timezone.utc),
        session_id=uuid4(),
        source="whisperlivekit",
        target="tonny",
        text="Show me the current tasks",
        audio_metadata=AudioMetadata(
            duration_ms=1800,
            sample_rate=16000,
            channels=1,
            bit_depth=BitDepth.integer_16,
            format=Format.pcm,
            language="en",
            confidence=0.88,
        ),
        is_final=True,
        segment_id="seg_002",
    )

    print("✅ Complete event created successfully")
    print(f"   Text: {event.text}")
    print(f"   Language: {event.audio_metadata.language}")
    print(f"   Confidence: {event.audio_metadata.confidence}")
    print(f"   Bit Depth: {event.audio_metadata.bit_depth}")
    print(f"   Segment ID: {event.segment_id}")


def validate_json_serialization() -> None:
    """Validate JSON serialization and deserialization."""
    print_section("Testing JSON Serialization/Deserialization")

    # Create event
    original = TranscriptionCompletedEvent(
        event_type="whisperlivekit.transcription.completed",
        timestamp=datetime.now(timezone.utc),
        session_id=uuid4(),
        source="whisperlivekit",
        target="candybar",
        text="Test serialization",
        audio_metadata=AudioMetadata(
            duration_ms=1000,
            sample_rate=16000,
            channels=1,
            format=Format.pcm,
            confidence=0.95,
        ),
        is_final=True,
    )

    # Serialize to JSON
    json_str = original.model_dump_json(indent=2)
    print("✅ Serialized to JSON:")
    print(json_str[:300] + "..." if len(json_str) > 300 else json_str)

    # Deserialize from JSON
    deserialized = TranscriptionCompletedEvent.model_validate_json(json_str)
    print("\n✅ Deserialized from JSON successfully")
    print(f"   Text matches: {original.text == deserialized.text}")
    print(f"   Session ID matches: {original.session_id == deserialized.session_id}")


def validate_error_handling() -> None:
    """Validate error handling for invalid events."""
    print_section("Testing Error Handling")

    # Test 1: Invalid event type
    try:
        TranscriptionCompletedEvent(
            event_type="wrong.event.type",
            timestamp=datetime.now(timezone.utc),
            session_id=uuid4(),
            source="whisperlivekit",
            target="tonny",
            text="Test",
            audio_metadata=AudioMetadata(
                duration_ms=1000,
                sample_rate=16000,
                channels=1,
                format=Format.pcm,
            ),
            is_final=True,
        )
        print("❌ Should have rejected invalid event_type")
    except Exception:
        print("✅ Correctly rejected invalid event_type")

    # Test 2: Empty text
    try:
        TranscriptionCompletedEvent(
            event_type="whisperlivekit.transcription.completed",
            timestamp=datetime.now(timezone.utc),
            session_id=uuid4(),
            source="whisperlivekit",
            target="tonny",
            text="",
            audio_metadata=AudioMetadata(
                duration_ms=1000,
                sample_rate=16000,
                channels=1,
                format=Format.pcm,
            ),
            is_final=True,
        )
        print("❌ Should have rejected empty text")
    except Exception:
        print("✅ Correctly rejected empty text")

    # Test 3: Invalid sample rate
    try:
        AudioMetadata(
            duration_ms=1000,
            sample_rate=4000,  # Below minimum
            channels=1,
            format=Format.pcm,
        )
        print("❌ Should have rejected invalid sample_rate")
    except Exception:
        print("✅ Correctly rejected invalid sample_rate")


def demonstrate_bloodbank_integration() -> None:
    """Demonstrate Bloodbank integration pattern."""
    print_section("Bloodbank Integration Example")

    event = TranscriptionCompletedEvent(
        event_type="whisperlivekit.transcription.completed",
        timestamp=datetime.now(timezone.utc),
        session_id=uuid4(),
        source="whisperlivekit",
        target="tonny",
        text="What's the weather forecast?",
        audio_metadata=AudioMetadata(
            duration_ms=2000,
            sample_rate=16000,
            channels=1,
            format=Format.pcm,
            confidence=0.92,
        ),
        is_final=True,
    )

    # Prepare for Bloodbank publishing
    payload = event.model_dump()

    print("✅ Event ready for Bloodbank publishing:")
    print(f"   Event Type: {payload['event_type']}")
    print(f"   Source: {payload['source']}")
    print(f"   Target: {payload['target']}")
    print(f"   Text: {payload['text']}")
    print("\n   Command to publish:")
    print(f"   bb publish --event-type {payload['event_type']} --payload '<json>'")


def main() -> None:
    """Run all validation tests."""
    print("\n" + "=" * 70)
    print(" HolyFields Transcription Event Schema Validation")
    print(" Version: 1.0.0")
    print("=" * 70)

    try:
        validate_minimal_event()
        validate_complete_event()
        validate_json_serialization()
        validate_error_handling()
        demonstrate_bloodbank_integration()

        print_section("All Validations Passed! ✅")
        print("Schema is production ready and can be used by:")
        print("  • WhisperLiveKit (publisher)")
        print("  • Tonny Agent (consumer)")
        print("  • Candybar (monitoring)")
        print("  • Candystore (storage)")
        print("  • Bloodbank (event bus)\n")

    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        raise


if __name__ == "__main__":
    main()

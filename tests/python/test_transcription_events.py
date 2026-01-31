"""Contract validation tests for WhisperLiveKit transcription events.

Tests validate that generated Pydantic models match JSON Schema expectations
for the transcription.completed event.
"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from holyfields.generated.python.whisperlivekit.events import (
    AudioMetadata,
    BaseVoiceEvent,
    BitDepth,
    Format,
    TranscriptionCompletedEvent,
)


class TestBaseVoiceEvent:
    """Test base voice event schema validation."""

    def test_valid_base_voice_event(self):
        """Test that a valid base voice event passes validation."""
        event = BaseVoiceEvent(
            event_type="whisperlivekit.transcription.completed",
            timestamp=datetime.now(timezone.utc),
            session_id=uuid4(),
            source="whisperlivekit",
            target="tonny",
        )
        assert event.event_type == "whisperlivekit.transcription.completed"
        assert event.source == "whisperlivekit"
        assert event.target == "tonny"
        assert isinstance(event.session_id, UUID)

    def test_invalid_event_type_pattern(self):
        """Test that invalid event_type pattern is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            BaseVoiceEvent(
                event_type="Invalid Event Type!",  # Should fail pattern validation
                timestamp=datetime.now(timezone.utc),
                session_id=uuid4(),
                source="whisperlivekit",
                target="tonny",
            )
        errors = exc_info.value.errors()
        assert any("pattern" in str(e).lower() for e in errors)

    def test_invalid_source_pattern(self):
        """Test that invalid source pattern is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            BaseVoiceEvent(
                event_type="whisperlivekit.transcription.completed",
                timestamp=datetime.now(timezone.utc),
                session_id=uuid4(),
                source="Invalid Source!",  # Should fail pattern validation
                target="tonny",
            )
        errors = exc_info.value.errors()
        assert any("pattern" in str(e).lower() for e in errors)

    def test_missing_required_fields(self):
        """Test that missing required fields are rejected."""
        with pytest.raises(ValidationError):
            BaseVoiceEvent(
                event_type="whisperlivekit.transcription.completed",
                # Missing timestamp, session_id, source, target
            )


class TestAudioMetadata:
    """Test audio metadata schema validation."""

    def test_valid_audio_metadata(self):
        """Test that valid audio metadata passes validation."""
        metadata = AudioMetadata(
            duration_ms=2500,
            sample_rate=16000,
            channels=1,
            bit_depth=BitDepth.integer_16,
            format=Format.pcm,
            language="en",
            confidence=0.95,
        )
        assert metadata.duration_ms == 2500
        assert metadata.sample_rate == 16000
        assert metadata.channels == 1
        assert metadata.bit_depth == BitDepth.integer_16
        assert metadata.format == Format.pcm
        assert metadata.language == "en"
        assert metadata.confidence == 0.95

    def test_duration_ms_minimum(self):
        """Test that negative duration_ms is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            AudioMetadata(
                duration_ms=-100,  # Should fail >= 0 constraint
                sample_rate=16000,
                channels=1,
                format=Format.pcm,
            )
        errors = exc_info.value.errors()
        assert any("greater_than_equal" in str(e).lower() for e in errors)

    def test_sample_rate_range(self):
        """Test that sample_rate outside valid range is rejected."""
        # Too low
        with pytest.raises(ValidationError):
            AudioMetadata(
                duration_ms=1000,
                sample_rate=4000,  # Should fail >= 8000 constraint
                channels=1,
                format=Format.pcm,
            )

        # Too high
        with pytest.raises(ValidationError):
            AudioMetadata(
                duration_ms=1000,
                sample_rate=96000,  # Should fail <= 48000 constraint
                channels=1,
                format=Format.pcm,
            )

    def test_channels_range(self):
        """Test that channels outside valid range is rejected."""
        with pytest.raises(ValidationError):
            AudioMetadata(
                duration_ms=1000,
                sample_rate=16000,
                channels=5,  # Should fail <= 2 constraint
                format=Format.pcm,
            )

    def test_confidence_range(self):
        """Test that confidence outside 0.0-1.0 range is rejected."""
        with pytest.raises(ValidationError):
            AudioMetadata(
                duration_ms=1000,
                sample_rate=16000,
                channels=1,
                format=Format.pcm,
                confidence=1.5,  # Should fail <= 1.0 constraint
            )

    def test_language_pattern(self):
        """Test that invalid language code is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            AudioMetadata(
                duration_ms=1000,
                sample_rate=16000,
                channels=1,
                format=Format.pcm,
                language="english",  # Should fail ^[a-z]{2}$ pattern
            )
        errors = exc_info.value.errors()
        assert any("pattern" in str(e).lower() for e in errors)


class TestTranscriptionCompletedEvent:
    """Test transcription completed event schema validation."""

    def test_valid_transcription_completed_event(self):
        """Test that a valid transcription completed event passes validation."""
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
                bit_depth=BitDepth.integer_16,
                format=Format.pcm,
                language="en",
                confidence=0.95,
            ),
            is_final=True,
            segment_id="seg_001",
        )
        assert event.event_type == "whisperlivekit.transcription.completed"
        assert event.text == "Hey Tonny, what's the weather like today?"
        assert event.is_final is True
        assert event.segment_id == "seg_001"

    def test_event_type_literal_constraint(self):
        """Test that event_type must be exact literal value."""
        with pytest.raises(ValidationError) as exc_info:
            TranscriptionCompletedEvent(
                event_type="wrong.event.type",  # Should fail literal constraint
                timestamp=datetime.now(timezone.utc),
                session_id=uuid4(),
                source="whisperlivekit",
                target="tonny",
                text="Test text",
                audio_metadata=AudioMetadata(
                    duration_ms=1000,
                    sample_rate=16000,
                    channels=1,
                    format=Format.pcm,
                ),
                is_final=True,
            )
        errors = exc_info.value.errors()
        assert any("literal" in str(e).lower() or "unexpected" in str(e).lower() for e in errors)

    def test_text_length_constraints(self):
        """Test that text length constraints are enforced."""
        # Empty text (min_length=1)
        with pytest.raises(ValidationError):
            TranscriptionCompletedEvent(
                event_type="whisperlivekit.transcription.completed",
                timestamp=datetime.now(timezone.utc),
                session_id=uuid4(),
                source="whisperlivekit",
                target="tonny",
                text="",  # Should fail min_length=1
                audio_metadata=AudioMetadata(
                    duration_ms=1000,
                    sample_rate=16000,
                    channels=1,
                    format=Format.pcm,
                ),
                is_final=True,
            )

        # Text too long (max_length=10000)
        with pytest.raises(ValidationError):
            TranscriptionCompletedEvent(
                event_type="whisperlivekit.transcription.completed",
                timestamp=datetime.now(timezone.utc),
                session_id=uuid4(),
                source="whisperlivekit",
                target="tonny",
                text="x" * 10001,  # Should fail max_length=10000
                audio_metadata=AudioMetadata(
                    duration_ms=1000,
                    sample_rate=16000,
                    channels=1,
                    format=Format.pcm,
                ),
                is_final=True,
            )

    def test_no_additional_properties(self):
        """Test that additional properties are rejected (additionalProperties: false)."""
        with pytest.raises(ValidationError) as exc_info:
            TranscriptionCompletedEvent(
                event_type="whisperlivekit.transcription.completed",
                timestamp=datetime.now(timezone.utc),
                session_id=uuid4(),
                source="whisperlivekit",
                target="tonny",
                text="Test text",
                audio_metadata=AudioMetadata(
                    duration_ms=1000,
                    sample_rate=16000,
                    channels=1,
                    format=Format.pcm,
                ),
                is_final=True,
                unexpected_field="should fail",  # Should fail additionalProperties: false
            )
        errors = exc_info.value.errors()
        assert any("extra" in str(e).lower() or "unexpected" in str(e).lower() for e in errors)

    def test_example_payload_from_schema(self):
        """Test that the example payload from schema is valid."""
        event = TranscriptionCompletedEvent(
            event_type="whisperlivekit.transcription.completed",
            timestamp=datetime.fromisoformat("2026-01-27T10:30:15.234000+00:00"),
            session_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            source="whisperlivekit",
            target="tonny",
            text="Hey Tonny, what's the weather like today?",
            audio_metadata=AudioMetadata(
                duration_ms=2500,
                sample_rate=16000,
                channels=1,
                bit_depth=BitDepth.integer_16,
                format=Format.pcm,
                language="en",
                confidence=0.95,
            ),
            is_final=True,
            segment_id="seg_001",
        )
        # Validate by serializing and deserializing
        json_data = event.model_dump_json()
        reloaded = TranscriptionCompletedEvent.model_validate_json(json_data)
        assert reloaded.text == event.text
        assert reloaded.session_id == event.session_id

    def test_optional_fields(self):
        """Test that optional fields can be omitted."""
        event = TranscriptionCompletedEvent(
            event_type="whisperlivekit.transcription.completed",
            timestamp=datetime.now(timezone.utc),
            session_id=uuid4(),
            source="whisperlivekit",
            target="tonny",
            text="Test text",
            audio_metadata=AudioMetadata(
                duration_ms=1000,
                sample_rate=16000,
                channels=1,
                format=Format.pcm,
                # Optional fields omitted: bit_depth, language, confidence
            ),
            is_final=True,
            # Optional field omitted: segment_id
        )
        assert event.text == "Test text"
        assert event.audio_metadata.language is None
        assert event.segment_id is None

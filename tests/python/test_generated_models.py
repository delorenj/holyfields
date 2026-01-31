"""Test generated Python Pydantic models for correctness.

Validates that generated models from JSON Schemas:
1. Can be instantiated with valid data
2. Enforce validation rules correctly
3. Match expected types and constraints
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from holyfields.generated.python.theboard.events import (
    CommentExtractedEvent,
    MeetingCompletedEvent,
    MeetingConvergedEvent,
    MeetingCreatedEvent,
    MeetingFailedEvent,
    MeetingStartedEvent,
    RoundCompletedEvent,
    TopComment,
)


class TestMeetingCreatedEvent:
    """Test MeetingCreatedEvent validation."""

    def test_valid_event(self):
        """Valid event should instantiate successfully."""
        event = MeetingCreatedEvent(
            event_type="meeting.created",
            timestamp=datetime.now(timezone.utc),
            meeting_id=uuid4(),
            topic="How can we improve AI safety?",
            strategy="multi_agent",
            max_rounds=5,
            agent_count=3,
        )
        assert event.event_type == "meeting.created"
        assert event.topic == "How can we improve AI safety?"
        assert event.strategy == "multi_agent"

    def test_strategy_enum_validation(self):
        """Invalid strategy should raise ValidationError."""
        with pytest.raises(ValidationError):
            MeetingCreatedEvent(
                event_type="meeting.created",
                timestamp=datetime.now(timezone.utc),
                meeting_id=uuid4(),
                topic="Test",
                strategy="invalid_strategy",  # Not in enum
                max_rounds=5,
            )

    def test_max_rounds_constraints(self):
        """max_rounds must be between 1 and 100."""
        # Too low
        with pytest.raises(ValidationError):
            MeetingCreatedEvent(
                event_type="meeting.created",
                timestamp=datetime.now(timezone.utc),
                meeting_id=uuid4(),
                topic="Test",
                strategy="simple",
                max_rounds=0,  # Below minimum
            )

        # Too high
        with pytest.raises(ValidationError):
            MeetingCreatedEvent(
                event_type="meeting.created",
                timestamp=datetime.now(timezone.utc),
                meeting_id=uuid4(),
                topic="Test",
                strategy="simple",
                max_rounds=101,  # Above maximum
            )

    def test_optional_agent_count(self):
        """agent_count should be optional (nullable)."""
        event = MeetingCreatedEvent(
            event_type="meeting.created",
            timestamp=datetime.now(timezone.utc),
            meeting_id=uuid4(),
            topic="Test",
            strategy="simple",
            max_rounds=5,
            agent_count=None,  # Should be allowed
        )
        assert event.agent_count is None


class TestCommentExtractedEvent:
    """Test CommentExtractedEvent validation."""

    def test_category_enum(self):
        """category must be valid enum value."""
        event = CommentExtractedEvent(
            event_type="meeting.comment_extracted",
            timestamp=datetime.now(timezone.utc),
            meeting_id=uuid4(),
            round_num=1,
            agent_name="Alice",
            comment_text="This is a test comment",
            category="recommendation",
            novelty_score=0.85,
        )
        assert event.category == "recommendation"

    def test_novelty_score_range(self):
        """novelty_score must be between 0.0 and 1.0."""
        # Valid range
        event = CommentExtractedEvent(
            event_type="meeting.comment_extracted",
            timestamp=datetime.now(timezone.utc),
            meeting_id=uuid4(),
            round_num=1,
            agent_name="Alice",
            comment_text="Test",
            category="idea",
            novelty_score=0.5,
        )
        assert event.novelty_score == 0.5

        # Below range
        with pytest.raises(ValidationError):
            CommentExtractedEvent(
                event_type="meeting.comment_extracted",
                timestamp=datetime.now(timezone.utc),
                meeting_id=uuid4(),
                round_num=1,
                agent_name="Alice",
                comment_text="Test",
                category="idea",
                novelty_score=-0.1,
            )

        # Above range
        with pytest.raises(ValidationError):
            CommentExtractedEvent(
                event_type="meeting.comment_extracted",
                timestamp=datetime.now(timezone.utc),
                meeting_id=uuid4(),
                round_num=1,
                agent_name="Alice",
                comment_text="Test",
                category="idea",
                novelty_score=1.5,
            )


class TestMeetingCompletedEvent:
    """Test MeetingCompletedEvent with nested TopComment."""

    def test_with_top_comments(self):
        """Event with top_comments should validate nested structure."""
        top_comment = TopComment(
            text="We should consider alignment with human values.",
            category="recommendation",
            novelty_score=0.92,
            agent_name="Alice",
            round_num=1,
        )

        event = MeetingCompletedEvent(
            event_type="meeting.completed",
            timestamp=datetime.now(timezone.utc),
            meeting_id=uuid4(),
            total_rounds=5,
            total_comments=18,
            total_cost=0.234,
            convergence_detected=True,
            stopping_reason="convergence",
            top_comments=[top_comment],
            category_distribution={"recommendation": 6, "question": 5},
            agent_participation={"Alice": 6, "Bob": 6, "Charlie": 6},
        )

        assert len(event.top_comments) == 1
        assert event.top_comments[0].agent_name == "Alice"
        assert event.top_comments[0].novelty_score == 0.92

    def test_top_comments_max_length(self):
        """top_comments limited to 5 items."""
        top_comments = [
            TopComment(
                text=f"Comment {i}",
                category="idea",
                novelty_score=0.8,
                agent_name="Alice",
                round_num=1,
            )
            for i in range(6)  # 6 comments (exceeds max of 5)
        ]

        with pytest.raises(ValidationError):
            MeetingCompletedEvent(
                event_type="meeting.completed",
                timestamp=datetime.now(timezone.utc),
                meeting_id=uuid4(),
                total_rounds=5,
                total_comments=18,
                total_cost=0.234,
                convergence_detected=True,
                stopping_reason="convergence",
                top_comments=top_comments,
                category_distribution={},
                agent_participation={},
            )


class TestMeetingFailedEvent:
    """Test MeetingFailedEvent with optional fields."""

    def test_with_optional_fields(self):
        """Optional round_num and agent_name should be nullable."""
        event = MeetingFailedEvent(
            event_type="meeting.failed",
            timestamp=datetime.now(timezone.utc),
            meeting_id=uuid4(),
            error_type="validation_error",
            error_message="Meeting topic cannot be empty",
            round_num=None,  # Should be allowed
            agent_name=None,  # Should be allowed
        )
        assert event.round_num is None
        assert event.agent_name is None

    def test_error_type_enum(self):
        """error_type must be valid enum value."""
        event = MeetingFailedEvent(
            event_type="meeting.failed",
            timestamp=datetime.now(timezone.utc),
            meeting_id=uuid4(),
            error_type="agent_error",
            error_message="Agent timeout",
            round_num=3,
            agent_name="Alice",
        )
        assert event.error_type == "agent_error"

        # Invalid enum value
        with pytest.raises(ValidationError):
            MeetingFailedEvent(
                event_type="meeting.failed",
                timestamp=datetime.now(timezone.utc),
                meeting_id=uuid4(),
                error_type="unknown_error_type",
                error_message="Test",
            )


class TestEventTypeDiscriminators:
    """Test event_type literal validation."""

    def test_event_type_enforced(self):
        """event_type must match literal value."""
        # Correct value
        event = MeetingCreatedEvent(
            event_type="meeting.created",
            timestamp=datetime.now(timezone.utc),
            meeting_id=uuid4(),
            topic="Test",
            strategy="simple",
            max_rounds=5,
        )
        assert event.event_type == "meeting.created"

        # Wrong value should fail
        with pytest.raises(ValidationError):
            MeetingCreatedEvent(
                event_type="wrong.type",  # Not matching literal
                timestamp=datetime.now(timezone.utc),
                meeting_id=uuid4(),
                topic="Test",
                strategy="simple",
                max_rounds=5,
            )

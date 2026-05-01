from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class TheboardMeetingCommentExtractedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class TheboardMeetingCommentExtractedV1Payload(BaseModel):
    round_num: int = Field(..., description='Round number when comment was extracted', ge=1)
    agent_name: str = Field(..., description='Agent who authored the comment')
    comment_text: str = Field(..., description='Extracted comment text', min_length=1, max_length=5000)
    category: Literal['technical_decision', 'risk', 'implementation_detail', 'observation', 'question', 'other'] = Field(..., description='Comment category classified by notetaker agent')
    novelty_score: float = Field(..., description='Novelty score (0.0 = repetitive, 1.0 = novel)', ge=0, le=1)
    meeting_id: str = Field(..., description='Unique meeting identifier')

class TheboardMeetingCommentExtractedV1(BaseModel):
    """Emitted when comments are extracted from agent response. Payload contains comment metadata for analytics."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['theboard.meeting.comment_extracted'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: TheboardMeetingCommentExtractedV1Source = Field(..., description='Metadata about the source that emitted this event')
    meeting_id: str = Field(..., description='UUID of the meeting this event relates to. Used for event correlation and tracing within TheBoard domain.')
    payload: TheboardMeetingCommentExtractedV1Payload

    EVENT_TYPE: ClassVar[str] = 'theboard.meeting.comment_extracted'


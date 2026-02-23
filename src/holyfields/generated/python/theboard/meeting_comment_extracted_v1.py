from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    round_num: int = Field(..., description="Round number when comment was extracted")
    agent_name: str = Field(..., description="Agent who authored the comment")
    comment_text: str = Field(..., description="Extracted comment text")
    category: str = Field(..., description="Comment category classified by notetaker agent")
    novelty_score: float = Field(..., description="Novelty score (0.0 = repetitive, 1.0 = novel)")


class TheboardMeetingCommentExtractedV1(BaseModel):
    """Emitted when comments are extracted from agent response. Payload contains comment metadata for analytics."""

    event_type: Literal["theboard.meeting.comment_extracted"] = "theboard.meeting.comment_extracted"
    payload: Payload

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class TheboardMeetingCommentExtractedV1(BaseModel):
    """Emitted when comments are extracted from agent response. Payload contains comment metadata for analytics."""

    round_num: int = Field(..., description="Round number when comment was extracted", ge=1)
    agent_name: str = Field(..., description="Agent who authored the comment")
    comment_text: str = Field(..., description="Extracted comment text", min_length=1, max_length=5000)
    category: Literal["technical_decision", "risk", "implementation_detail", "observation", "question", "other"] = Field(..., description="Comment category classified by notetaker agent")
    novelty_score: float = Field(..., description="Novelty score (0.0 = repetitive, 1.0 = novel)", ge=0, le=1)
    meeting_id: str = Field(..., description="Unique meeting identifier")

    EVENT_TYPE: str = "theboard.meeting.comment_extracted"

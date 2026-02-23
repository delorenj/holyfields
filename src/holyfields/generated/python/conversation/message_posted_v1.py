from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class ConversationMessagePostedV1(BaseModel):
    """Emitted when a message is posted in a conversation"""

    conversation_id: str = Field(..., description="UUID of the conversation")
    message_id: str = Field(..., description="UUID of this message")
    author_id: str = Field(..., description="ID of the author (user or agent)")
    content: str = Field(..., description="The message content")
    reply_to_id: Optional[Any] = Field(None, description="ID of the message this is replying to")

    EVENT_TYPE: str = "conversation.message.posted"

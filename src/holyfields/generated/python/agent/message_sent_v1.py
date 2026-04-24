from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AgentMessageSentV1(BaseModel):
    """Outbound response sent by an agent"""

    agent_name: str = Field(..., description="Name of the agent that sent the message")
    channel: str = Field(..., description="Channel the message was sent to")
    message_preview: str = Field(..., description="First 200 characters of the response", max_length=200)
    message_length: int = Field(..., description="Total length of the response in characters", ge=0)
    model: Optional[str] = Field(None, description="AI model used to generate the response")
    tokens_used: Optional[int] = Field(None, description="Total tokens consumed (input + output)", ge=0)
    duration_ms: Optional[int] = Field(None, description="Time to generate response in milliseconds", ge=0)

    EVENT_TYPE: str = "agent.message.sent"

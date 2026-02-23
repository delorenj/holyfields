from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    agent_name: str = Field(..., description="Name of the agent that received the message")
    channel: str = Field(..., description="Channel the message came from")
    sender: str = Field(..., description="User name or ID who sent the message")
    message_preview: str = Field(..., description="First 200 characters of the message")
    message_length: int = Field(..., description="Total length of the message in characters")
    session_key: str = Field(..., description="Session identifier (e.g., 'agent:main:main')")


class AgentMessageReceivedV1(BaseModel):
    """Inbound message received by an agent"""

    event_type: Literal["agent.message.received"] = "agent.message.received"
    payload: Payload

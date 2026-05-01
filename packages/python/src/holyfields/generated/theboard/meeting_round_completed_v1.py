from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class TheboardMeetingRoundCompletedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class TheboardMeetingRoundCompletedV1Payload(BaseModel):
    round_num: int = Field(..., description='Round number that just completed', ge=1)
    agent_name: str = Field(..., description='Name of agent who contributed in this round')
    response_length: int = Field(..., description="Character length of agent's response", ge=0)
    comment_count: int = Field(..., description='Number of comments extracted from response', ge=0)
    avg_novelty: float = Field(..., description='Average novelty score of extracted comments (0.0 = repetitive, 1.0 = novel)', ge=0, le=1)
    tokens_used: int = Field(..., description='Total tokens consumed (input + output)', ge=0)
    cost: float = Field(..., description="Cost in USD for this round's LLM calls", ge=0)
    meeting_id: str = Field(..., description='Unique meeting identifier')

class TheboardMeetingRoundCompletedV1(BaseModel):
    """Emitted when a meeting round completes. Payload contains round metrics and convergence indicators."""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['theboard.meeting.round_completed'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: TheboardMeetingRoundCompletedV1Source = Field(..., description='Metadata about the source that emitted this event')
    meeting_id: str = Field(..., description='UUID of the meeting this event relates to. Used for event correlation and tracing within TheBoard domain.')
    payload: TheboardMeetingRoundCompletedV1Payload

    EVENT_TYPE: ClassVar[str] = 'theboard.meeting.round_completed'


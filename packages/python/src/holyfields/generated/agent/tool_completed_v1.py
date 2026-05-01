from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentToolCompletedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentToolCompletedV1Payload(BaseModel):
    agent_name: str = Field(..., description='Name of the agent that invoked the tool')
    tool_name: str = Field(..., description='Name of the tool')
    success: bool = Field(..., description='Whether the tool completed successfully')
    duration_ms: int | None = Field(None, description='Tool execution time in milliseconds', ge=0)
    output_preview: str | None = Field(None, description='First 200 characters of tool output', max_length=200)

class AgentToolCompletedV1(BaseModel):
    """Agent tool call finished"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.tool.completed'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentToolCompletedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentToolCompletedV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.tool.completed'


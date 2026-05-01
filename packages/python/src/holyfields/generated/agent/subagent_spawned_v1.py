from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentSubagentSpawnedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentSubagentSpawnedV1Payload(BaseModel):
    agent_name: str = Field(..., description='Name of the parent agent')
    child_label: str = Field(..., description="Sub-agent label (e.g., 'worker-1')")
    child_session_key: str = Field(..., description='Session key of the spawned sub-agent')
    task_preview: str = Field(..., description='First 200 characters of the delegated task', max_length=200)
    model: str | None = Field(None, description='AI model assigned to the sub-agent')

class AgentSubagentSpawnedV1(BaseModel):
    """Agent delegated work to a sub-agent"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.subagent.spawned'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentSubagentSpawnedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentSubagentSpawnedV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.subagent.spawned'


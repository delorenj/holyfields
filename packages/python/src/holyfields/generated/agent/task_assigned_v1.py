from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentTaskAssignedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class AgentTaskAssignedV1Payload(BaseModel):
    agent_name: str = Field(..., description='Name of the agent the task is assigned to')
    source: str = Field(..., description="Who assigned the task (e.g., 'plane', 'cack', 'jarad')")
    task_type: Literal['ticket', 'message', 'cron', 'adhoc'] = Field(..., description='Type of task')
    task_preview: str = Field(..., description='First 200 characters of the task description', max_length=200)

class AgentTaskAssignedV1(BaseModel):
    """External task routed to an agent"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['agent.task.assigned'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: AgentTaskAssignedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: AgentTaskAssignedV1Payload

    EVENT_TYPE: ClassVar[str] = 'agent.task.assigned'


from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class GithubPrCreatedV1Source(BaseModel):
    """Metadata about the source that emitted this event"""

    host: str = Field(..., description='Hostname of the emitting machine')
    app: str = Field(..., description="Application or service name (e.g., 'bloodbank', 'holocene', 'cack')")
    trigger_type: Literal['cli', 'api', 'scheduled', 'event', 'webhook'] = Field(..., description='What triggered this event')
    user_id: str | None = Field(None, description='User or agent ID if applicable')

class GithubPrCreatedV1Payload(BaseModel):
    cache_key: str = Field(..., description="Key to retrieve PR data from cache (e.g., 'owner/repo/123')")
    cache_type: Literal['redis', 'memory', 'file'] | None = Field(None, description='Type of cache storage')
    repo_owner: str = Field(..., description='Repository owner')
    repo_name: str = Field(..., description='Repository name')
    pr_number: int = Field(..., description='Pull request number', ge=1)

class GithubPrCreatedV1(BaseModel):
    """GitHub pull request was created"""

    event_id: str = Field(..., description='Unique identifier for this event instance')
    event_type: Literal['github.pr.created'] = Field(..., description='Event type discriminator')
    timestamp: str = Field(..., description='ISO 8601 UTC timestamp when event was emitted')
    version: str = Field(..., description='Schema version for this event type')
    correlation_id: str = Field(..., description='UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.')
    causation_id: str | None = Field(None, description='ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.')
    source: GithubPrCreatedV1Source = Field(..., description='Metadata about the source that emitted this event')
    payload: GithubPrCreatedV1Payload

    EVENT_TYPE: ClassVar[str] = 'github.pr.created'


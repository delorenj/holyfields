from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentSessionStartedV1Data(BaseModel):
    """Session-start payload."""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., description='Stable identifier for this session. Used as the correlation key for all downstream agent.* events from the same session.')
    working_directory: str = Field(..., description='Absolute path the agent is operating in at session start. Captured once; subsequent cd within tools is not reflected here.', min_length=1)
    git_branch: str | None = Field(None, description='Git branch the agent is on at session start. Empty string when not in a git repo.')
    git_remote: str | None = Field(None, description="Origin remote URL for the working_directory's repo. Empty string when not in a git repo or when no origin is configured.")
    started_at: str = Field(..., description='RFC3339 UTC timestamp at which the session began. Producers should set this to match the envelope `time` field.')

class AgentSessionStartedV1(BaseModel):
    """Emitted when an agent session begins. Producer is typically the agent runtime itself (e.g., Claude Code via .claude/hooks/bloodbank-publisher.sh on SessionStart). Consumers track session lifecycle, attribute downstream events to a session, and aggregate per-session metrics."""

    specversion: Literal['1.0'] = Field(..., description="CloudEvents specification version. Always '1.0' for v3.")
    id: str = Field(..., description='Unique identifier for this event. Consumers dedup on this. Set by producer; Dapr preserves.')
    source: str = Field(..., description="Event source as URI-reference. Convention: 'urn:33god:service:<service-name>' or 'urn:33god:cli:<tool-name>' for operator-issued events.", min_length=1)
    type: Literal['agent.session.started'] = Field(..., description='Locked event type for this schema.')
    subject: str | None = Field(None, description="Event subject. Convention: '<entity>/<id>'. Optional at the CloudEvents layer; strongly recommended for 33GOD so consumers can filter without parsing data.", min_length=1)
    time: str = Field(..., description='RFC3339 UTC timestamp when the event was produced. Preserved verbatim on replay.')
    datacontenttype: str = Field('application/json', description="MIME type of the data field. 33GOD default is 'application/json'.")
    dataschema: str | None = Field(None, description="Apicurio registry URI identifying the schema that validates data. Convention: 'apicurio://holyfields/<type>/versions/<n>'.")
    correlationid: str = Field(..., description='Correlation ID for causal chains. All events in one logical workflow share the same correlationid.')
    causationid: str | None = Field(None, description='ID of the event or command that directly caused this one. Null for root events. Together with correlationid forms a DAG of causation.')
    producer: str = Field(..., description="Canonical producer identity. Agent name, service ID, or 'operator:<name>' for human-issued events.", min_length=1)
    service: str = Field(..., description='The service that emitted this event. Matches the service registry entry name.', min_length=1)
    domain: Literal['agent'] = Field(..., description='Locked domain for this schema.')
    schemaref: str | None = Field(None, description='Short schema reference, distinct from dataschema (which is the full URI). Useful for log / trace contexts where the URI is too noisy.', min_length=1)
    traceparent: str | None = Field(None, description="W3C Trace Context traceparent header. Zero-trace placeholder is '00-00000000000000000000000000000000-0000000000000000-00'.", pattern='^[0-9a-f]{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$')
    data: AgentSessionStartedV1Data = Field(..., description='Session-start payload.')

    EVENT_TYPE: ClassVar[str] = 'agent.session.started'


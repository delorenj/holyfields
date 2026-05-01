from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentSubagentCompletedV1Data(BaseModel):
    """Subagent-completion payload."""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., description='Identifier of the PARENT session that spawned the subagent. Subagent activity rolls up under this session.')
    agent_type: str | None = Field(None, description="Type/name of the subagent that finished (e.g. 'general-purpose', 'demo-architect'). Producer-defined; treat unknown values as opaque.")
    stop_reason: Literal['completed', 'error', 'timeout', 'user_stop'] = Field(..., description='Why the subagent ended. completed: returned a result. error: unrecoverable failure. timeout: idle/total budget exceeded. user_stop: explicit termination.')
    working_directory: str | None = Field(None, description='Absolute path the parent session was operating in when the subagent finished.')

class AgentSubagentCompletedV1(BaseModel):
    """Emitted when a subagent (a Task-tool spawned helper) finishes. Producer is the agent runtime (e.g. Claude Code via .claude/hooks/bloodbank-publisher.sh on SubagentStop). Distinct from agent.session.ended: the parent session continues; only the subagent has terminated. The session_id field points to the PARENT session so subagent activity rolls up under the originating session."""

    specversion: Literal['1.0'] = Field(..., description="CloudEvents specification version. Always '1.0' for v3.")
    id: str = Field(..., description='Unique identifier for this event. Consumers dedup on this. Set by producer; Dapr preserves.')
    source: str = Field(..., description="Event source as URI-reference. Convention: 'urn:33god:service:<service-name>' or 'urn:33god:cli:<tool-name>' for operator-issued events.", min_length=1)
    type: Literal['agent.subagent.completed'] = Field(..., description='Locked event type for this schema.')
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
    data: AgentSubagentCompletedV1Data = Field(..., description='Subagent-completion payload.')

    EVENT_TYPE: ClassVar[str] = 'agent.subagent.completed'


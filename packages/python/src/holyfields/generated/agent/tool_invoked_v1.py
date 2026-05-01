from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentToolInvokedV1Data(BaseModel):
    """Tool-invocation payload."""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., description='Identifier of the session that issued this tool call. Matches session_id from the corresponding agent.session.started event.')
    tool_name: str = Field(..., description="Name of the tool the agent invoked (e.g., 'Bash', 'Read', 'Edit', 'Grep'). Producer-defined; consumers should treat unknown names as opaque rather than enum-restricted.", min_length=1, max_length=200)
    tool_input: dict[str, Any] | None = Field(None, description='Raw tool-specific input as supplied by the agent. Schema is per-tool and intentionally not constrained here. Producers may redact or truncate at their discretion.')
    working_directory: str | None = Field(None, description='Absolute path the agent was operating in when the tool fired. Captured from session state, not re-evaluated per tool call.')
    git_branch: str | None = Field(None, description='Git branch at invocation time. Empty string when not in a git repo.')
    git_status: Literal['clean', 'modified'] | None = Field(None, description='Coarse git working-tree state. clean: no uncommitted changes. modified: at least one tracked file diverges from HEAD.')
    turn_number: int = Field(..., description='1-based turn counter within the session. Increments on every tool invocation.', ge=1)
    success: bool | None = Field(None, description="Producer's optimistic success flag at publish time. PostToolUse hooks fire AFTER the tool ran but cannot observe agent-level interpretation; treat false as authoritative, true as best-effort.")

class AgentToolInvokedV1(BaseModel):
    """Emitted when an agent invokes a tool. One event per invocation. Carries enough context (tool name, raw input, session, repo state) for downstream observability without persisting full conversation history. The tool_input field is opaque on purpose: each tool defines its own input shape and this schema does not constrain it."""

    specversion: Literal['1.0'] = Field(..., description="CloudEvents specification version. Always '1.0' for v3.")
    id: str = Field(..., description='Unique identifier for this event. Consumers dedup on this. Set by producer; Dapr preserves.')
    source: str = Field(..., description="Event source as URI-reference. Convention: 'urn:33god:service:<service-name>' or 'urn:33god:cli:<tool-name>' for operator-issued events.", min_length=1)
    type: Literal['agent.tool.invoked'] = Field(..., description='Locked event type for this schema.')
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
    data: AgentToolInvokedV1Data = Field(..., description='Tool-invocation payload.')

    EVENT_TYPE: ClassVar[str] = 'agent.tool.invoked'


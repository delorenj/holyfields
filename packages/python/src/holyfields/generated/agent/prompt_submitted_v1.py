from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentPromptSubmittedV1Data(BaseModel):
    """Prompt-submission payload."""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., description='Identifier of the session the prompt belongs to. Matches the session_id from the corresponding agent.session.started event.')
    prompt_text: str = Field(..., description='Raw prompt text as submitted by the user. May be truncated by the producer at its discretion; see prompt_length for the original size before any truncation.')
    prompt_length: int = Field(..., description='Character length of the original prompt before any truncation. Lets consumers detect truncation by comparing against `len(prompt_text)`.', ge=0)
    working_directory: str | None = Field(None, description='Absolute path the agent is operating in at prompt-submit time.')
    git_branch: str | None = Field(None, description='Git branch at prompt-submit time. Empty string when not in a git repo.')

class AgentPromptSubmittedV1(BaseModel):
    """Emitted when a user submits a prompt to an agent. Producer is the agent runtime (e.g. Claude Code via .claude/hooks/bloodbank-publisher.sh on UserPromptSubmit). Carries the raw prompt text alongside repo state at submission time. Consumers use it to attribute downstream tool invocations to a user intent and to build retrospective views of what was asked."""

    specversion: Literal['1.0'] = Field(..., description="CloudEvents specification version. Always '1.0' for v3.")
    id: str = Field(..., description='Unique identifier for this event. Consumers dedup on this. Set by producer; Dapr preserves.')
    source: str = Field(..., description="Event source as URI-reference. Convention: 'urn:33god:service:<service-name>' or 'urn:33god:cli:<tool-name>' for operator-issued events.", min_length=1)
    type: Literal['agent.prompt.submitted'] = Field(..., description='Locked event type for this schema.')
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
    data: AgentPromptSubmittedV1Data = Field(..., description='Prompt-submission payload.')

    EVENT_TYPE: ClassVar[str] = 'agent.prompt.submitted'


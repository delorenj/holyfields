from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AgentSessionEndedV1Data(BaseModel):
    """Session-end payload with aggregate session statistics."""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., description='Identifier of the session that just ended. Matches the session_id from the corresponding agent.session.started event.')
    end_reason: Literal['user_stop', 'completed', 'error', 'timeout', 'context_full'] = Field(..., description='Why the session ended. user_stop: explicit termination. completed: agent finished its work. error: unrecoverable failure. timeout: idle/total budget exceeded. context_full: hit token limit.')
    duration_seconds: int = Field(..., description='Wall-clock seconds between session start and end.', ge=0)
    total_turns: int = Field(..., description='Number of agent turns (tool invocations + responses) during the session.', ge=0)
    tools_used: dict[str, int] | None = Field(None, description='Histogram mapping tool name to invocation count for the session.')
    files_modified: list[str] | None = Field(None, description='Repository-relative paths that were modified (uncommitted) at session end. Best-effort; reflects `git diff --name-only` at the moment the session ended.')
    git_commits: list[str] | None = Field(None, description='Commit SHAs created during the session, ordered most-recent first. Best-effort; reflects `git log --since=<started_at>` at the moment the session ended.')
    final_status: Literal['success', 'failure', 'partial'] | None = Field(None, description='Outcome classifier. success: goals achieved. failure: blocked or aborted. partial: some goals met.')
    working_directory: str | None = Field(None, description='Absolute path the session ran in. Mirrors the value from agent.session.started.', min_length=1)
    git_branch: str | None = Field(None, description='Git branch at session end. May differ from session.started if the agent switched branches mid-session.')

class AgentSessionEndedV1(BaseModel):
    """Emitted when an agent session terminates. Carries summary statistics of the session (turn count, tool histogram, files touched, commits created) so consumers can build retrospective views without replaying every agent.tool.invoked event."""

    specversion: Literal['1.0'] = Field(..., description="CloudEvents specification version. Always '1.0' for v3.")
    id: str = Field(..., description='Unique identifier for this event. Consumers dedup on this. Set by producer; Dapr preserves.')
    source: str = Field(..., description="Event source as URI-reference. Convention: 'urn:33god:service:<service-name>' or 'urn:33god:cli:<tool-name>' for operator-issued events.", min_length=1)
    type: Literal['agent.session.ended'] = Field(..., description='Locked event type for this schema.')
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
    data: AgentSessionEndedV1Data = Field(..., description='Session-end payload with aggregate session statistics.')

    EVENT_TYPE: ClassVar[str] = 'agent.session.ended'


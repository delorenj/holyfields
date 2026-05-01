from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class SystemHeartbeatTickV1Data(BaseModel):
    """Heartbeat-specific payload."""

    model_config = ConfigDict(extra="forbid")

    tick_seq: int = Field(..., description='Monotonically increasing sequence number from the producer instance. Resets to 0 on producer restart; consumers detect restarts by combining with `started_at`.', ge=0)
    interval_ms: int | None = Field(None, description='Configured interval between ticks at the producer, in milliseconds. Advisory only; consumers must not assume the next tick will arrive within this window.', ge=100)
    producer_id: str = Field(..., description="Stable identifier for this producer instance. Convention: '<service-name>:<replica-id>' or a UUID generated at startup.", min_length=1, max_length=200)
    started_at: str = Field(..., description='Time the producer instance started. Combined with `producer_id`, lets consumers detect restarts and order overlapping tick streams.')

class SystemHeartbeatTickV1(BaseModel):
    """Periodic heartbeat event emitted by a tick service. Consumers use it for liveness monitoring, scheduled task fan-out, restart detection, and as a synthetic load source for testing the v3 event platform. The first real-world domain event in the v3 ecosystem; pattern reference for future domain events."""

    specversion: Literal['1.0'] = Field(..., description="CloudEvents specification version. Always '1.0' for v3.")
    id: str = Field(..., description='Unique identifier for this event. Consumers dedup on this. Set by producer; Dapr preserves.')
    source: str = Field(..., description="Event source as URI-reference. Convention: 'urn:33god:service:<service-name>' or 'urn:33god:cli:<tool-name>' for operator-issued events.", min_length=1)
    type: Literal['system.heartbeat.tick'] = Field(..., description='Locked event type for this schema.')
    subject: str | None = Field(None, description="Event subject. Convention: '<entity>/<id>'. Optional at the CloudEvents layer; strongly recommended for 33GOD so consumers can filter without parsing data.", min_length=1)
    time: str = Field(..., description='RFC3339 UTC timestamp when the event was produced. Preserved verbatim on replay.')
    datacontenttype: str = Field('application/json', description="MIME type of the data field. 33GOD default is 'application/json'.")
    dataschema: str | None = Field(None, description="Apicurio registry URI identifying the schema that validates data. Convention: 'apicurio://holyfields/<type>/versions/<n>'.")
    correlationid: str = Field(..., description='Correlation ID for causal chains. All events in one logical workflow share the same correlationid.')
    causationid: str | None = Field(None, description='ID of the event or command that directly caused this one. Null for root events. Together with correlationid forms a DAG of causation.')
    producer: str = Field(..., description="Canonical producer identity. Agent name, service ID, or 'operator:<name>' for human-issued events.", min_length=1)
    service: str = Field(..., description='The service that emitted this event. Matches the service registry entry name.', min_length=1)
    domain: Literal['system'] = Field(..., description='Locked domain for this schema.')
    schemaref: str | None = Field(None, description='Short schema reference, distinct from dataschema (which is the full URI). Useful for log / trace contexts where the URI is too noisy.', min_length=1)
    traceparent: str | None = Field(None, description="W3C Trace Context traceparent header. Zero-trace placeholder is '00-00000000000000000000000000000000-0000000000000000-00'.", pattern='^[0-9a-f]{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$')
    data: SystemHeartbeatTickV1Data = Field(..., description='Heartbeat-specific payload.')

    EVENT_TYPE: ClassVar[str] = 'system.heartbeat.tick'


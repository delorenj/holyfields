# `_common/` — Shared base schemas

Schemas in this directory are **referenced** by other schemas via
`allOf: [{ "$ref": "..." }]`. They are intentionally **skipped** by the Pydantic /
Zod generators; the child schemas that extend them inline the parent fields in
the generated output.

## Which base to use

| Base | When to use |
|---|---|
| [`base_event.v1.json`](./base_event.v1.json) | **Legacy v2** events published on the RabbitMQ path (`bloodbank.events.v1` exchange). Snake_case fields (`event_id`, `event_type`, `correlation_id`), nested `source` object. |
| [`cloudevent_base.v1.json`](./cloudevent_base.v1.json) | **v3** events published through Dapr + NATS JetStream. CloudEvents 1.0 shape (`id`, `type`, `source` URI string) plus 33GOD extension fields (`correlationid`, `producer`, `service`, `domain`, `schemaref`, `traceparent`). |

Both coexist. Services that still live on the v2 RabbitMQ path continue to use
`base_event.v1.json`. Services that publish through v3 Dapr should `allOf` ref
`cloudevent_base.v1.json` and make their domain-specific payload the `data`
field.

## Rationale for the v3 base

See the metarepo audit at
`../../../../docs/architecture/holyfields-cloudevents-audit-2026-04-24.md`
(relative from `_common/`) and ADR-0001 + ADR-0002 for the full reasoning.

One-liner: v2 base fields do not satisfy CloudEvents 1.0 at the wire level, so
Dapr wraps our v2 envelope in its own CloudEvents envelope, producing two sets
of IDs and two correlation concepts. The v3 base IS a CloudEvents envelope; it
round-trips verbatim through Dapr.

## Example: extending the v3 base

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://33god.dev/schemas/weather/reading.recorded.v1.json",
  "title": "Weather Reading Recorded",
  "type": "object",
  "allOf": [{ "$ref": "../_common/cloudevent_base.v1.json" }],
  "properties": {
    "type":   { "const": "weather.reading.recorded" },
    "domain": { "const": "weather" },
    "data": {
      "type": "object",
      "properties": {
        "sensor_id": { "$ref": "../_common/types.v1.json#/$defs/uuid" },
        "temperature_c": { "type": "number" },
        "recorded_at": { "$ref": "../_common/types.v1.json#/$defs/timestamp" }
      },
      "required": ["sensor_id", "temperature_c", "recorded_at"]
    }
  },
  "required": ["data"]
}
```

Constants on `type` and `domain` give per-schema narrow types in the generated
Pydantic / Zod models so services can't accidentally construct mismatched
envelopes.

## `types.v1.json`

Shared primitive types (`uuid`, `timestamp`, `semantic_version`, etc.). Referenced
from both base schemas and from most domain schemas. Do not duplicate these
patterns in child schemas; always `$ref` here.

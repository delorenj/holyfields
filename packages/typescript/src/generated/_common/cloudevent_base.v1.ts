import { z } from "zod"

/**CloudEvents 1.0 envelope with 33GOD extension fields. Per ADR-0001, this is the wire-level shape for all v3 events published through Dapr + NATS JetStream. Legacy v2 events (RabbitMQ path) continue to use base_event.v1.json. See holyfields-cloudevents-audit-2026-04-24.md in the metarepo for rationale.*/
export const CommonCloudeventBaseV1Schema = z.object({ 
/**CloudEvents specification version. Always '1.0' for v3.*/
"specversion": z.literal("1.0").describe("CloudEvents specification version. Always '1.0' for v3."), 
/**Unique identifier for this event. Consumers dedup on this. Set by producer; Dapr preserves.*/
"id": z.any().describe("Unique identifier for this event. Consumers dedup on this. Set by producer; Dapr preserves."), 
/**Event source as URI-reference. Convention: 'urn:33god:service:<service-name>' or 'urn:33god:cli:<tool-name>' for operator-issued events.*/
"source": z.string().min(1).describe("Event source as URI-reference. Convention: 'urn:33god:service:<service-name>' or 'urn:33god:cli:<tool-name>' for operator-issued events."), 
/**Dotted event type. Convention: '<domain>.<entity>.<action>'. Also used as the Dapr topic name (and therefore the NATS subject) by convention 'event.<type>'.*/
"type": z.string().regex(new RegExp("^[a-z0-9]+(\\.[a-z0-9]+)+$")).min(1).describe("Dotted event type. Convention: '<domain>.<entity>.<action>'. Also used as the Dapr topic name (and therefore the NATS subject) by convention 'event.<type>'."), 
/**Event subject. Convention: '<entity>/<id>'. Optional at the CloudEvents layer; strongly recommended for 33GOD so consumers can filter without parsing data.*/
"subject": z.string().min(1).describe("Event subject. Convention: '<entity>/<id>'. Optional at the CloudEvents layer; strongly recommended for 33GOD so consumers can filter without parsing data.").optional(), 
/**RFC3339 UTC timestamp when the event was produced. Preserved verbatim on replay.*/
"time": z.any().describe("RFC3339 UTC timestamp when the event was produced. Preserved verbatim on replay."), 
/**MIME type of the data field. 33GOD default is 'application/json'.*/
"datacontenttype": z.string().describe("MIME type of the data field. 33GOD default is 'application/json'.").default("application/json"), 
/**Apicurio registry URI identifying the schema that validates data. Convention: 'apicurio://holyfields/<type>/versions/<n>'.*/
"dataschema": z.string().describe("Apicurio registry URI identifying the schema that validates data. Convention: 'apicurio://holyfields/<type>/versions/<n>'.").optional(), 
/**Correlation ID for causal chains. All events in one logical workflow share the same correlationid.*/
"correlationid": z.any().describe("Correlation ID for causal chains. All events in one logical workflow share the same correlationid."), 
/**ID of the event or command that directly caused this one. Null for root events. Together with correlationid forms a DAG of causation.*/
"causationid": z.any().superRefine((x, ctx) => {
    const schemas = [z.any(), z.null()];
    const errors = schemas.reduce<z.ZodError[]>(
      (errors, schema) =>
        ((result) =>
          result.error ? [...errors, result.error] : errors)(
          schema.safeParse(x),
        ),
      [],
    );
    if (schemas.length - errors.length !== 1) {
      ctx.addIssue({
        path: ctx.path,
        code: "invalid_union",
        unionErrors: errors,
        message: "Invalid input: Should pass single schema",
      });
    }
  }).describe("ID of the event or command that directly caused this one. Null for root events. Together with correlationid forms a DAG of causation.").default(null), 
/**Canonical producer identity. Agent name, service ID, or 'operator:<name>' for human-issued events.*/
"producer": z.string().min(1).describe("Canonical producer identity. Agent name, service ID, or 'operator:<name>' for human-issued events."), 
/**The service that emitted this event. Matches the service registry entry name.*/
"service": z.string().min(1).describe("The service that emitted this event. Matches the service registry entry name."), 
/**The domain this event belongs to. Typically the first segment of 'type'.*/
"domain": z.string().min(1).describe("The domain this event belongs to. Typically the first segment of 'type'."), 
/**Short schema reference, distinct from dataschema (which is the full URI). Useful for log / trace contexts where the URI is too noisy.*/
"schemaref": z.string().min(1).describe("Short schema reference, distinct from dataschema (which is the full URI). Useful for log / trace contexts where the URI is too noisy.").optional(), 
/**W3C Trace Context traceparent header. Zero-trace placeholder is '00-00000000000000000000000000000000-0000000000000000-00'.*/
"traceparent": z.string().regex(new RegExp("^[0-9a-f]{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$")).describe("W3C Trace Context traceparent header. Zero-trace placeholder is '00-00000000000000000000000000000000-0000000000000000-00'.").optional(), 
/**Domain-specific event payload. Validated separately by the domain schema identified by dataschema / schemaref.*/
"data": z.record(z.any()).describe("Domain-specific event payload. Validated separately by the domain schema identified by dataschema / schemaref.") }).describe("CloudEvents 1.0 envelope with 33GOD extension fields. Per ADR-0001, this is the wire-level shape for all v3 events published through Dapr + NATS JetStream. Legacy v2 events (RabbitMQ path) continue to use base_event.v1.json. See holyfields-cloudevents-audit-2026-04-24.md in the metarepo for rationale.")
export type CommonCloudeventBaseV1 = z.infer<typeof CommonCloudeventBaseV1Schema>

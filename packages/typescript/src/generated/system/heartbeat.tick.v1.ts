import { z } from "zod"

/**Periodic heartbeat event emitted by a tick service. Consumers use it for liveness monitoring, scheduled task fan-out, restart detection, and as a synthetic load source for testing the v3 event platform. The first real-world domain event in the v3 ecosystem; pattern reference for future domain events.*/
export const SystemHeartbeatTickV1Schema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("system.heartbeat.tick").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("system").describe("Locked domain for this schema.").optional(), 
/**Heartbeat-specific payload.*/
"data": z.object({ 
/**Monotonically increasing sequence number from the producer instance. Resets to 0 on producer restart; consumers detect restarts by combining with `started_at`.*/
"tick_seq": z.number().int().gte(0).describe("Monotonically increasing sequence number from the producer instance. Resets to 0 on producer restart; consumers detect restarts by combining with `started_at`."), 
/**Configured interval between ticks at the producer, in milliseconds. Advisory only; consumers must not assume the next tick will arrive within this window.*/
"interval_ms": z.number().int().gte(100).describe("Configured interval between ticks at the producer, in milliseconds. Advisory only; consumers must not assume the next tick will arrive within this window.").optional(), 
/**Stable identifier for this producer instance. Convention: '<service-name>:<replica-id>' or a UUID generated at startup.*/
"producer_id": z.string().min(1).max(200).describe("Stable identifier for this producer instance. Convention: '<service-name>:<replica-id>' or a UUID generated at startup."), 
/**Time the producer instance started. Combined with `producer_id`, lets consumers detect restarts and order overlapping tick streams.*/
"started_at": z.any().describe("Time the producer instance started. Combined with `producer_id`, lets consumers detect restarts and order overlapping tick streams.") }).strict().describe("Heartbeat-specific payload.") }).and(z.any()).describe("Periodic heartbeat event emitted by a tick service. Consumers use it for liveness monitoring, scheduled task fan-out, restart detection, and as a synthetic load source for testing the v3 event platform. The first real-world domain event in the v3 ecosystem; pattern reference for future domain events.")
export type SystemHeartbeatTickV1 = z.infer<typeof SystemHeartbeatTickV1Schema>

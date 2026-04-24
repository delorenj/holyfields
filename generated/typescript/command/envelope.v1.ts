import { z } from "zod"

/**Wire-level envelope for commands sent to agents via Bloodbank. Commands are imperative ('do X'), unlike events which are declarative ('X happened').*/
export const EnvelopeEventSchema = z.object({ 
/**Base event_type for command envelope. Actual routing uses command.{agent}.{action}.*/
"event_type": z.literal("command.envelope").describe("Base event_type for command envelope. Actual routing uses command.{agent}.{action}."), "payload": z.object({ 
/**Unique ID for this command instance. Used for idempotency, ack/result correlation.*/
"command_id": z.any().describe("Unique ID for this command instance. Used for idempotency, ack/result correlation."), 
/**Agent that should execute this command.*/
"target_agent": z.any().describe("Agent that should execute this command."), 
/**Identity of the command issuer (agent name, 'system', or human name).*/
"issued_by": z.string().min(1).describe("Identity of the command issuer (agent name, 'system', or human name)."), 
/**Command action identifier (e.g., 'run_drift_check', 'assign_ticket').*/
"action": z.string().min(1).describe("Command action identifier (e.g., 'run_drift_check', 'assign_ticket')."), 
/**Execution priority. 'critical' bypasses queue ordering.*/
"priority": z.enum(["low","normal","high","critical"]).describe("Execution priority. 'critical' bypasses queue ordering.").default("normal"), 
/**Time-to-live in ms. Command rejected if not acked within TTL. 0 = no expiry.*/
"ttl_ms": z.number().int().gte(0).describe("Time-to-live in ms. Command rejected if not acked within TTL. 0 = no expiry.").default(30000), 
/**Optional dedup key. Duplicates within 300s window get outcome='skipped'.*/
"idempotency_key": z.union([z.string().describe("Optional dedup key. Duplicates within 300s window get outcome='skipped'."), z.null().describe("Optional dedup key. Duplicates within 300s window get outcome='skipped'.")]).describe("Optional dedup key. Duplicates within 300s window get outcome='skipped'.").default(null), 
/**Action-specific data. Schema varies by action.*/
"command_payload": z.record(z.string(), z.any()).describe("Action-specific data. Schema varies by action.") }) }).and(z.any()).describe("Wire-level envelope for commands sent to agents via Bloodbank. Commands are imperative ('do X'), unlike events which are declarative ('X happened').")
export type EnvelopeEvent = z.infer<typeof EnvelopeEventSchema>

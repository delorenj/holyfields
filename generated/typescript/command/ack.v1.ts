import { z } from "zod"

/**Emitted immediately when an agent accepts a command for processing. Indicates the command passed all guards (TTL, idempotency, FSM state).*/
export const AckEventSchema = z.object({ 
/**Base event_type. Actual routing: command.{agent}.{action}.ack*/
"event_type": z.literal("command.ack").describe("Base event_type. Actual routing: command.{agent}.{action}.ack"), "payload": z.object({ 
/**ID of the command being acknowledged.*/
"command_id": z.any().describe("ID of the command being acknowledged."), 
/**Agent that accepted the command.*/
"target_agent": z.any().describe("Agent that accepted the command."), 
/**The command action being acknowledged.*/
"action": z.string().describe("The command action being acknowledged."), 
/**Optional estimate of execution time in milliseconds.*/
"estimated_duration_ms": z.union([z.number().int().gte(0).describe("Optional estimate of execution time in milliseconds."), z.null().describe("Optional estimate of execution time in milliseconds.")]).describe("Optional estimate of execution time in milliseconds.").default(null), 
/**FSM version after the acknowledging transition.*/
"fsm_version": z.number().int().gte(1).describe("FSM version after the acknowledging transition.") }) }).and(z.any()).describe("Emitted immediately when an agent accepts a command for processing. Indicates the command passed all guards (TTL, idempotency, FSM state).")
export type AckEvent = z.infer<typeof AckEventSchema>

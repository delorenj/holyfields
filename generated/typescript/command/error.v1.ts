import { z } from "zod"

/**Emitted when a command fails. Contains machine-readable classification and retry guidance.*/
export const ErrorEventSchema = z.object({ 
/**Base event_type. Actual routing: command.{agent}.{action}.error*/
"event_type": z.literal("command.error").describe("Base event_type. Actual routing: command.{agent}.{action}.error"), "payload": z.object({ 
/**ID of the command that failed.*/
"command_id": z.any().describe("ID of the command that failed."), 
/**Agent that attempted the command.*/
"target_agent": z.any().describe("Agent that attempted the command."), 
/**The command action that failed.*/
"action": z.string().describe("The command action that failed."), 
/**Machine-readable error classification.*/
"error_code": z.enum(["timeout","rejected","invalid_state","execution_failed","not_implemented","ttl_expired","rate_limited"]).describe("Machine-readable error classification."), 
/**Human-readable error description.*/
"error_message": z.string().describe("Human-readable error description."), 
/**Whether the command can be retried.*/
"retryable": z.boolean().describe("Whether the command can be retried.").default(false), 
/**Suggested retry delay in ms. Only meaningful when retryable=true.*/
"retry_after_ms": z.union([z.number().int().gte(0).describe("Suggested retry delay in ms. Only meaningful when retryable=true."), z.null().describe("Suggested retry delay in ms. Only meaningful when retryable=true.")]).describe("Suggested retry delay in ms. Only meaningful when retryable=true.").default(null), 
/**FSM version after error transition. Null if error before FSM engagement (e.g., TTL expiry).*/
"fsm_version": z.union([z.number().int().gte(1).describe("FSM version after error transition. Null if error before FSM engagement (e.g., TTL expiry)."), z.null().describe("FSM version after error transition. Null if error before FSM engagement (e.g., TTL expiry).")]).describe("FSM version after error transition. Null if error before FSM engagement (e.g., TTL expiry).").default(null) }) }).and(z.any()).describe("Emitted when a command fails. Contains machine-readable classification and retry guidance.")
export type ErrorEvent = z.infer<typeof ErrorEventSchema>

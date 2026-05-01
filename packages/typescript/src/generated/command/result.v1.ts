import { z } from "zod"

/**Emitted when an agent completes command execution. Contains outcome classification and optional result data.*/
export const CommandResultV1Schema = z.object({ 
/**Base event_type. Actual routing: command.{agent}.{action}.result*/
"event_type": z.literal("command.result").describe("Base event_type. Actual routing: command.{agent}.{action}.result"), "payload": z.object({ 
/**ID of the command that produced this result.*/
"command_id": z.any().describe("ID of the command that produced this result."), 
/**Agent that executed the command.*/
"target_agent": z.any().describe("Agent that executed the command."), 
/**The command action that was executed.*/
"action": z.string().describe("The command action that was executed."), 
/**'success': completed fully. 'partial': completed with caveats. 'skipped': idempotency dedup, no work done.*/
"outcome": z.enum(["success","partial","skipped"]).describe("'success': completed fully. 'partial': completed with caveats. 'skipped': idempotency dedup, no work done."), 
/**Execution time from ack to result in milliseconds.*/
"duration_ms": z.union([z.number().int().gte(0).describe("Execution time from ack to result in milliseconds."), z.null().describe("Execution time from ack to result in milliseconds.")]).describe("Execution time from ack to result in milliseconds.").default(null), 
/**Action-specific result data. Null for skipped outcomes.*/
"result_payload": z.union([z.record(z.any()).describe("Action-specific result data. Null for skipped outcomes."), z.null().describe("Action-specific result data. Null for skipped outcomes.")]).describe("Action-specific result data. Null for skipped outcomes.").default(null), 
/**FSM version after transitioning back to idle.*/
"fsm_version": z.number().int().gte(1).describe("FSM version after transitioning back to idle.") }) }).and(z.any()).describe("Emitted when an agent completes command execution. Contains outcome classification and optional result data.")
export type CommandResultV1 = z.infer<typeof CommandResultV1Schema>

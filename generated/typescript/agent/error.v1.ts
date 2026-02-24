import { z } from "zod"

/**Error occurred in agent processing*/
export const ErrorEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.error").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the agent that encountered the error*/
"agent_name": z.any().describe("Name of the agent that encountered the error"), 
/**Category of error (e.g., 'rate_limit', 'timeout', 'internal')*/
"error_type": z.string().describe("Category of error (e.g., 'rate_limit', 'timeout', 'internal')"), 
/**Human-readable error message*/
"error_message": z.string().describe("Human-readable error message"), 
/**What was happening when the error occurred*/
"context": z.union([z.string().describe("What was happening when the error occurred"), z.null().describe("What was happening when the error occurred")]).describe("What was happening when the error occurred").optional() }) }).and(z.any()).describe("Error occurred in agent processing")
export type ErrorEvent = z.infer<typeof ErrorEventSchema>

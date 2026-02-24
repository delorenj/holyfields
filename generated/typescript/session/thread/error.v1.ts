import { z } from "zod"

/**Error occurred during session*/
export const ErrorEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("session.thread.error").describe("Event type discriminator"), "payload": z.object({ "session_id": z.string(), "thread_id": z.union([z.string(), z.null()]).optional(), "error_type": z.string(), "error_message": z.string(), "stack_trace": z.union([z.string(), z.null()]).optional(), "tool_name": z.union([z.string(), z.null()]).optional(), "recoverable": z.boolean().optional(), "turn_number": z.union([z.number().int(), z.null()]).optional() }) }).and(z.any()).describe("Error occurred during session")
export type ErrorEvent = z.infer<typeof ErrorEventSchema>

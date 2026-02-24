import { z } from "zod"

/**User message or assistant response in session*/
export const MessageEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("session.thread.message").describe("Event type discriminator"), "payload": z.object({ "session_id": z.string(), "thread_id": z.union([z.string(), z.null()]).optional(), "role": z.string(), "content": z.string(), "turn_number": z.number().int(), "tokens": z.union([z.number().int(), z.null()]).optional(), "model": z.union([z.string(), z.null()]).optional(), "thinking_included": z.boolean().optional(), "tool_calls": z.array(z.string()).optional() }) }).and(z.any()).describe("User message or assistant response in session")
export type MessageEvent = z.infer<typeof MessageEventSchema>

import { z } from "zod"

/**Claude Code thinking/reasoning event*/
export const ThinkingEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("session.thread.agent.thinking").describe("Event type discriminator"), "payload": z.object({ "session_id": z.string(), "thread_id": z.union([z.string(), z.null()]).optional(), "thinking_text": z.string(), "thinking_duration_ms": z.union([z.number().int(), z.null()]).optional(), "turn_number": z.union([z.number().int(), z.null()]).optional(), "triggered_by_tool": z.union([z.string(), z.null()]).optional() }) }).and(z.any()).describe("Claude Code thinking/reasoning event")
export type ThinkingEvent = z.infer<typeof ThinkingEventSchema>

import { z } from "zod"

/**A prompt is sent to an agent thread*/
export const PromptEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.thread.prompt").describe("Event type discriminator"), "payload": z.object({ "provider": z.string(), "model": z.union([z.string(), z.null()]).optional(), "prompt": z.string(), "project": z.union([z.string(), z.null()]).optional(), "working_dir": z.union([z.string(), z.null()]).optional(), "domain": z.union([z.string(), z.null()]).optional(), "tags": z.array(z.string()).optional() }) }).and(z.any()).describe("A prompt is sent to an agent thread")
export type PromptEvent = z.infer<typeof PromptEventSchema>

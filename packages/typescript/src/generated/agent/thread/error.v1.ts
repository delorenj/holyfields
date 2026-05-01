import { z } from "zod"

/**Agent interaction failed*/
export const AgentThreadErrorV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.thread.error").describe("Event type discriminator"), "payload": z.object({ "provider": z.string(), "model": z.union([z.string(), z.null()]).optional(), "error_message": z.string(), "error_code": z.union([z.string(), z.null()]).optional(), "is_retryable": z.boolean().optional(), "retry_count": z.number().int().optional() }) }).and(z.any()).describe("Agent interaction failed")
export type AgentThreadErrorV1 = z.infer<typeof AgentThreadErrorV1Schema>

import { z } from "zod"

/**Agent responded to prompt*/
export const AgentThreadResponseV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.thread.response").describe("Event type discriminator"), "payload": z.object({ "provider": z.string(), 
/**Deprecated - use correlation_ids*/
"prompt_id": z.union([z.string().describe("Deprecated - use correlation_ids"), z.null().describe("Deprecated - use correlation_ids")]).describe("Deprecated - use correlation_ids").optional(), "response": z.string(), "model": z.union([z.string(), z.null()]).optional(), "tokens_used": z.union([z.number().int(), z.null()]).optional(), "duration_ms": z.union([z.number().int(), z.null()]).optional() }) }).and(z.any()).describe("Agent responded to prompt")
export type AgentThreadResponseV1 = z.infer<typeof AgentThreadResponseV1Schema>

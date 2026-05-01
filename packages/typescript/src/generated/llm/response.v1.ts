import { z } from "zod"

/**[DEPRECATED] Use agent.thread.response instead. LLM responded to prompt.*/
export const LlmResponseV1Schema = z.object({ 
/**Event type discriminator - DEPRECATED*/
"event_type": z.literal("llm.response").describe("Event type discriminator - DEPRECATED"), "payload": z.object({ 
/**LLM provider*/
"provider": z.string().describe("LLM provider"), 
/**Response text*/
"response": z.string().describe("Response text"), 
/**Model used*/
"model": z.union([z.string().describe("Model used"), z.null().describe("Model used")]).describe("Model used").optional(), 
/**Tokens consumed*/
"tokens_used": z.union([z.number().int().gte(0).describe("Tokens consumed"), z.null().describe("Tokens consumed")]).describe("Tokens consumed").optional(), 
/**Response time*/
"duration_ms": z.union([z.number().int().gte(0).describe("Response time"), z.null().describe("Response time")]).describe("Response time").optional(), 
/**Deprecation notice*/
"_deprecated": z.literal("Use agent.thread.response instead").describe("Deprecation notice").optional() }) }).and(z.any()).describe("[DEPRECATED] Use agent.thread.response instead. LLM responded to prompt.")
export type LlmResponseV1 = z.infer<typeof LlmResponseV1Schema>

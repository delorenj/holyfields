import { z } from "zod"

/**[DEPRECATED] Use agent.thread.error instead. LLM interaction failed.*/
export const LlmErrorV1Schema = z.object({ 
/**Event type discriminator - DEPRECATED*/
"event_type": z.literal("llm.error").describe("Event type discriminator - DEPRECATED"), "payload": z.object({ 
/**LLM provider*/
"provider": z.string().describe("LLM provider"), 
/**Error message*/
"error_message": z.string().describe("Error message"), 
/**Model being used*/
"model": z.union([z.string().describe("Model being used"), z.null().describe("Model being used")]).describe("Model being used").optional(), 
/**Error code*/
"error_code": z.union([z.string().describe("Error code"), z.null().describe("Error code")]).describe("Error code").optional(), 
/**Whether error is retryable*/
"is_retryable": z.boolean().describe("Whether error is retryable").optional(), 
/**Retry attempts*/
"retry_count": z.number().int().gte(0).describe("Retry attempts").optional(), 
/**Deprecation notice*/
"_deprecated": z.literal("Use agent.thread.error instead").describe("Deprecation notice").optional() }) }).and(z.any()).describe("[DEPRECATED] Use agent.thread.error instead. LLM interaction failed.")
export type LlmErrorV1 = z.infer<typeof LlmErrorV1Schema>

import { z } from "zod"

/**[DEPRECATED] Use agent.thread.prompt instead. LLM interaction started.*/
export const PromptEventSchema = z.object({ 
/**Event type discriminator - DEPRECATED*/
"event_type": z.literal("llm.prompt").describe("Event type discriminator - DEPRECATED"), "payload": z.object({ 
/**LLM provider*/
"provider": z.string().describe("LLM provider"), 
/**Model name*/
"model": z.union([z.string().describe("Model name"), z.null().describe("Model name")]).describe("Model name").optional(), 
/**Prompt text*/
"prompt": z.string().describe("Prompt text"), 
/**Git project name*/
"project": z.union([z.string().describe("Git project name"), z.null().describe("Git project name")]).describe("Git project name").optional(), 
/**Tags*/
"tags": z.array(z.string()).describe("Tags").optional(), 
/**Deprecation notice*/
"_deprecated": z.literal("Use agent.thread.prompt instead").describe("Deprecation notice").optional() }) }).and(z.any()).describe("[DEPRECATED] Use agent.thread.prompt instead. LLM interaction started.")
export type PromptEvent = z.infer<typeof PromptEventSchema>

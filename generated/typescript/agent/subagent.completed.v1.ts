import { z } from "zod"

/**Sub-agent finished its work*/
export const SubagentCompletedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.subagent.completed").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the parent agent*/
"agent_name": z.any().describe("Name of the parent agent"), 
/**Sub-agent label*/
"child_label": z.string().describe("Sub-agent label"), 
/**Session key of the sub-agent*/
"child_session_key": z.any().describe("Session key of the sub-agent"), 
/**Whether the sub-agent completed successfully*/
"success": z.boolean().describe("Whether the sub-agent completed successfully"), 
/**Time the sub-agent ran in milliseconds*/
"duration_ms": z.number().int().gte(0).describe("Time the sub-agent ran in milliseconds").optional(), 
/**First 200 characters of the result*/
"result_preview": z.union([z.string().max(200).describe("First 200 characters of the result"), z.null().describe("First 200 characters of the result")]).describe("First 200 characters of the result").optional() }) }).and(z.any()).describe("Sub-agent finished its work")
export type SubagentCompletedEvent = z.infer<typeof SubagentCompletedEventSchema>

import { z } from "zod"

/**Agent delegated work to a sub-agent*/
export const SubagentSpawnedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.subagent.spawned").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the parent agent*/
"agent_name": z.any().describe("Name of the parent agent"), 
/**Sub-agent label (e.g., 'worker-1')*/
"child_label": z.string().describe("Sub-agent label (e.g., 'worker-1')"), 
/**Session key of the spawned sub-agent*/
"child_session_key": z.any().describe("Session key of the spawned sub-agent"), 
/**First 200 characters of the delegated task*/
"task_preview": z.string().max(200).describe("First 200 characters of the delegated task"), 
/**AI model assigned to the sub-agent*/
"model": z.any().describe("AI model assigned to the sub-agent").optional() }) }).and(z.any()).describe("Agent delegated work to a sub-agent")
export type SubagentSpawnedEvent = z.infer<typeof SubagentSpawnedEventSchema>

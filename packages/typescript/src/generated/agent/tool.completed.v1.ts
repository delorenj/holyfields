import { z } from "zod"

/**Agent tool call finished*/
export const AgentToolCompletedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.tool.completed").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the agent that invoked the tool*/
"agent_name": z.any().describe("Name of the agent that invoked the tool"), 
/**Name of the tool*/
"tool_name": z.string().describe("Name of the tool"), 
/**Whether the tool completed successfully*/
"success": z.boolean().describe("Whether the tool completed successfully"), 
/**Tool execution time in milliseconds*/
"duration_ms": z.number().int().gte(0).describe("Tool execution time in milliseconds").optional(), 
/**First 200 characters of tool output*/
"output_preview": z.union([z.string().max(200).describe("First 200 characters of tool output"), z.null().describe("First 200 characters of tool output")]).describe("First 200 characters of tool output").optional() }) }).and(z.any()).describe("Agent tool call finished")
export type AgentToolCompletedV1 = z.infer<typeof AgentToolCompletedV1Schema>

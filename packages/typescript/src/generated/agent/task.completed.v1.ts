import { z } from "zod"

/**Agent finished an assigned task*/
export const AgentTaskCompletedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.task.completed").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the agent that completed the task*/
"agent_name": z.any().describe("Name of the agent that completed the task"), 
/**Type of task*/
"task_type": z.enum(["ticket","message","cron","adhoc"]).describe("Type of task"), 
/**Whether the task completed successfully*/
"success": z.boolean().describe("Whether the task completed successfully"), 
/**Time to complete the task in milliseconds*/
"duration_ms": z.number().int().gte(0).describe("Time to complete the task in milliseconds").optional() }) }).and(z.any()).describe("Agent finished an assigned task")
export type AgentTaskCompletedV1 = z.infer<typeof AgentTaskCompletedV1Schema>

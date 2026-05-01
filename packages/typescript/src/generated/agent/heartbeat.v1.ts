import { z } from "zod"

/**Periodic agent health signal*/
export const AgentHeartbeatV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.heartbeat").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the agent*/
"agent_name": z.any().describe("Name of the agent"), 
/**Current agent status*/
"status": z.enum(["ok","busy","error","degraded"]).describe("Current agent status"), 
/**Number of active sessions*/
"active_sessions": z.number().int().gte(0).describe("Number of active sessions").optional(), 
/**Agent uptime in milliseconds*/
"uptime_ms": z.number().int().gte(0).describe("Agent uptime in milliseconds").optional() }) }).and(z.any()).describe("Periodic agent health signal")
export type AgentHeartbeatV1 = z.infer<typeof AgentHeartbeatV1Schema>

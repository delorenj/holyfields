import { z } from "zod"

/**Request feedback from a specific agent*/
export const RequestedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.feedback.requested").describe("Event type discriminator"), "payload": z.object({ 
/**AgentForge registry ID*/
"agent_id": z.string().describe("AgentForge registry ID"), 
/**Message to send to the agent*/
"message": z.string().describe("Message to send to the agent"), 
/**Optional Letta agent ID override*/
"letta_agent_id": z.union([z.string().describe("Optional Letta agent ID override"), z.null().describe("Optional Letta agent ID override")]).describe("Optional Letta agent ID override").optional(), 
/**Optional context for the agent*/
"context": z.record(z.any()).describe("Optional context for the agent").optional(), 
/**Tags for this feedback request*/
"tags": z.array(z.string()).describe("Tags for this feedback request").optional() }) }).and(z.any()).describe("Request feedback from a specific agent")
export type RequestedEvent = z.infer<typeof RequestedEventSchema>

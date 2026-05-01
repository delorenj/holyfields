import { z } from "zod"

/**Inbound message received by an agent*/
export const AgentMessageReceivedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.message.received").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the agent that received the message*/
"agent_name": z.any().describe("Name of the agent that received the message"), 
/**Channel the message came from*/
"channel": z.any().describe("Channel the message came from"), 
/**User name or ID who sent the message*/
"sender": z.string().describe("User name or ID who sent the message"), 
/**First 200 characters of the message*/
"message_preview": z.string().max(200).describe("First 200 characters of the message"), 
/**Total length of the message in characters*/
"message_length": z.number().int().gte(0).describe("Total length of the message in characters"), 
/**Session identifier (e.g., 'agent:main:main')*/
"session_key": z.any().describe("Session identifier (e.g., 'agent:main:main')") }) }).and(z.any()).describe("Inbound message received by an agent")
export type AgentMessageReceivedV1 = z.infer<typeof AgentMessageReceivedV1Schema>

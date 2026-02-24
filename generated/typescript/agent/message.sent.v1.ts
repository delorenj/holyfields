import { z } from "zod"

/**Outbound response sent by an agent*/
export const MessageSentEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.message.sent").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the agent that sent the message*/
"agent_name": z.any().describe("Name of the agent that sent the message"), 
/**Channel the message was sent to*/
"channel": z.any().describe("Channel the message was sent to"), 
/**First 200 characters of the response*/
"message_preview": z.string().max(200).describe("First 200 characters of the response"), 
/**Total length of the response in characters*/
"message_length": z.number().int().gte(0).describe("Total length of the response in characters"), 
/**AI model used to generate the response*/
"model": z.any().describe("AI model used to generate the response").optional(), 
/**Total tokens consumed (input + output)*/
"tokens_used": z.number().int().gte(0).describe("Total tokens consumed (input + output)").optional(), 
/**Time to generate response in milliseconds*/
"duration_ms": z.number().int().gte(0).describe("Time to generate response in milliseconds").optional() }) }).and(z.any()).describe("Outbound response sent by an agent")
export type MessageSentEvent = z.infer<typeof MessageSentEventSchema>

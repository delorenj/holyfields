import { z } from "zod"

/**Agent session closed*/
export const SessionEndedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.session.ended").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the agent*/
"agent_name": z.any().describe("Name of the agent"), 
/**Session identifier*/
"session_key": z.any().describe("Session identifier"), 
/**Reason the session ended*/
"reason": z.enum(["timeout","completion","error","manual"]).describe("Reason the session ended").optional(), 
/**Total session duration in milliseconds*/
"duration_ms": z.number().int().gte(0).describe("Total session duration in milliseconds").optional(), 
/**Total messages exchanged in this session*/
"total_messages": z.number().int().gte(0).describe("Total messages exchanged in this session").optional() }) }).and(z.any()).describe("Agent session closed")
export type SessionEndedEvent = z.infer<typeof SessionEndedEventSchema>

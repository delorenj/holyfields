import { z } from "zod"

/**New agent session began*/
export const SessionStartedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.session.started").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the agent*/
"agent_name": z.any().describe("Name of the agent"), 
/**Session identifier*/
"session_key": z.any().describe("Session identifier"), 
/**Channel the session is on*/
"channel": z.any().describe("Channel the session is on").optional(), 
/**AI model used in this session*/
"model": z.any().describe("AI model used in this session").optional() }) }).and(z.any()).describe("New agent session began")
export type SessionStartedEvent = z.infer<typeof SessionStartedEventSchema>

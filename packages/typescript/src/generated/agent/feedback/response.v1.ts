import { z } from "zod"

/**Agent feedback response*/
export const AgentFeedbackResponseV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.feedback.response").describe("Event type discriminator"), "payload": z.object({ 
/**AgentForge registry ID*/
"agent_id": z.string().describe("AgentForge registry ID"), 
/**Letta agent ID if different*/
"letta_agent_id": z.union([z.string().describe("Letta agent ID if different"), z.null().describe("Letta agent ID if different")]).describe("Letta agent ID if different").optional(), 
/**Agent's response text*/
"response": z.string().describe("Agent's response text"), 
/**Response status*/
"status": z.enum(["ok","error"]).describe("Response status"), 
/**Error message if status is error*/
"error_message": z.union([z.string().describe("Error message if status is error"), z.null().describe("Error message if status is error")]).describe("Error message if status is error").optional(), 
/**Additional metadata*/
"metadata": z.record(z.any()).describe("Additional metadata").optional() }) }).and(z.any()).describe("Agent feedback response")
export type AgentFeedbackResponseV1 = z.infer<typeof AgentFeedbackResponseV1Schema>

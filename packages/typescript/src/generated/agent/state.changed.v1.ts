import { z } from "zod"

/**Emitted when an agent changes its internal state or thinking process*/
export const AgentStateChangedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.state.changed").describe("Event type discriminator"), "payload": z.object({ 
/**ID of the agent whose state changed*/
"agent_id": z.any().describe("ID of the agent whose state changed"), 
/**Current state*/
"state": z.enum(["idle","thinking","working","error","paused"]).describe("Current state"), 
/**Internal monologue or reasoning (optional)*/
"thought_process": z.union([z.string().describe("Internal monologue or reasoning (optional)"), z.null().describe("Internal monologue or reasoning (optional)")]).describe("Internal monologue or reasoning (optional)").optional() }) }).and(z.any()).describe("Emitted when an agent changes its internal state or thinking process")
export type AgentStateChangedV1 = z.infer<typeof AgentStateChangedV1Schema>

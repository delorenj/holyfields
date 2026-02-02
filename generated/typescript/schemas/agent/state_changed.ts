import { z } from "zod"

/**Emitted when an agent changes its internal state or thinking process*/
export const agentStateChangedEventSchema = z.object({ "event_type": z.literal("agent.state.changed"), "timestamp": z.any(), "agent_id": z.string(), 
/**Current state (e.g. 'thinking', 'idle', 'working')*/
"state": z.string().describe("Current state (e.g. 'thinking', 'idle', 'working')"), 
/**Internal monologue or reasoning*/
"thought_process": z.string().describe("Internal monologue or reasoning").optional() }).describe("Emitted when an agent changes its internal state or thinking process")
export type AgentStateChangedEvent = z.infer<typeof agentStateChangedEventSchema>

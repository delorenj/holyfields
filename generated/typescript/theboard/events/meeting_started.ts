import { z } from "zod"
import { baseEventSchema } from "../../base_event.js"

/**Emitted when a meeting transitions to RUNNING status. Payload contains selected agents and execution configuration.*/
export const meetingStartedEventSchema = baseEventSchema.extend({ 
/**Event type discriminator*/
"event_type": z.literal("meeting.started").describe("Event type discriminator"), 
/**Names of AI agents selected for this meeting*/
"selected_agents": z.array(z.string().min(1)).min(1).describe("Names of AI agents selected for this meeting"), 
/**Total number of agents (redundant with array length, kept for backward compatibility)*/
"agent_count": z.number().int().gte(1).describe("Total number of agents (redundant with array length, kept for backward compatibility)") }).describe("Emitted when a meeting transitions to RUNNING status. Payload contains selected agents and execution configuration.")
export type MeetingStartedEvent = z.infer<typeof meetingStartedEventSchema>

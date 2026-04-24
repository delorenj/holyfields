import { z } from "zod"

/**Emitted when a meeting transitions to RUNNING status. Payload contains selected agents and execution configuration.*/
export const MeetingStartedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("theboard.meeting.started").describe("Event type discriminator"), "payload": z.object({ 
/**Names of AI agents selected for this meeting*/
"selected_agents": z.array(z.any()).min(1).refine((arr) => arr.every((item, i) => arr.indexOf(item) == i), "All items must be unique!").describe("Names of AI agents selected for this meeting"), 
/**Total number of agents participating*/
"agent_count": z.number().int().gte(1).describe("Total number of agents participating"), 
/**Unique meeting identifier*/
"meeting_id": z.any().describe("Unique meeting identifier") }) }).and(z.intersection(z.any(), z.any())).describe("Emitted when a meeting transitions to RUNNING status. Payload contains selected agents and execution configuration.")
export type MeetingStartedEvent = z.infer<typeof MeetingStartedEventSchema>

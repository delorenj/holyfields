import { z } from "zod"
import { baseEventSchema } from "../../base_event.js"

/**Emitted when a new meeting is created. Payload contains initial meeting configuration.*/
export const meetingCreatedEventSchema = baseEventSchema.extend({ 
/**Event type discriminator*/
"event_type": z.literal("meeting.created").describe("Event type discriminator"), 
/**Meeting topic or question to discuss*/
"topic": z.string().min(1).max(1000).describe("Meeting topic or question to discuss"), 
/**Meeting execution strategy*/
"strategy": z.enum(["simple","multi_agent"]).describe("Meeting execution strategy"), 
/**Maximum number of discussion rounds before stopping*/
"max_rounds": z.number().int().gte(1).lte(100).describe("Maximum number of discussion rounds before stopping"), 
/**Number of agents participating (null if not yet selected)*/
"agent_count": z.union([z.number().int().gte(1).describe("Number of agents participating (null if not yet selected)"), z.null().describe("Number of agents participating (null if not yet selected)")]).describe("Number of agents participating (null if not yet selected)").optional() }).describe("Emitted when a new meeting is created. Payload contains initial meeting configuration.")
export type MeetingCreatedEvent = z.infer<typeof meetingCreatedEventSchema>

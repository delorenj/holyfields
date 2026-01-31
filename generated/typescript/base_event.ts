import { z } from "zod"

/**Base schema for all TheBoard events. Provides common fields for event routing, tracing, and correlation. All component events extend this base.*/
export const baseEventSchema = z.object({ 
/**Event discriminator for routing (e.g., 'theboard.meeting.created'). Used by Bloodbank for topic-based routing.*/
"event_type": z.string().regex(new RegExp("^[a-z0-9]+\\.[a-z0-9._]+$")).describe("Event discriminator for routing (e.g., 'theboard.meeting.created'). Used by Bloodbank for topic-based routing."), 
/**ISO 8601 UTC timestamp when event was emitted*/
"timestamp": z.string().datetime().describe("ISO 8601 UTC timestamp when event was emitted"), 
/**UUID of the meeting this event relates to. Used for event correlation and tracing.*/
"meeting_id": z.string().uuid().describe("UUID of the meeting this event relates to. Used for event correlation and tracing.") }).describe("Base schema for all TheBoard events. Provides common fields for event routing, tracing, and correlation. All component events extend this base.")
export type BaseEvent = z.infer<typeof baseEventSchema>

import { z } from "zod"
import { baseEventSchema } from "../../base_event.js"

/**Emitted when meeting execution fails. Payload contains error context for debugging.*/
export const meetingFailedEventSchema = baseEventSchema.extend({ 
/**Event type discriminator*/
"event_type": z.literal("meeting.failed").describe("Event type discriminator"), 
/**Category of error that caused failure*/
"error_type": z.enum(["agent_error","timeout","network_error","validation_error","internal_error"]).describe("Category of error that caused failure"), 
/**Human-readable error message for debugging*/
"error_message": z.string().min(1).max(2000).describe("Human-readable error message for debugging"), 
/**Round number when failure occurred (null if before meeting started)*/
"round_num": z.union([z.any(), z.null()]).describe("Round number when failure occurred (null if before meeting started)").optional(), 
/**Agent that caused the error (null if not agent-specific)*/
"agent_name": z.union([z.any(), z.null()]).describe("Agent that caused the error (null if not agent-specific)").optional() }).describe("Emitted when meeting execution fails. Payload contains error context for debugging.")
export type MeetingFailedEvent = z.infer<typeof meetingFailedEventSchema>

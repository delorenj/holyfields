import { z } from "zod"
import { baseEventSchema } from "../../base_event.js"

/**Emitted when meeting reaches convergence. Payload contains convergence metrics and stopping criteria.*/
export const meetingConvergedEventSchema = baseEventSchema.extend({ 
/**Event type discriminator*/
"event_type": z.literal("meeting.converged").describe("Event type discriminator"), 
/**Round number when convergence detected*/
"round_num": z.any().describe("Round number when convergence detected"), 
/**Average novelty score that triggered convergence*/
"avg_novelty": z.any().describe("Average novelty score that triggered convergence"), 
/**Novelty threshold for convergence detection*/
"novelty_threshold": z.any().describe("Novelty threshold for convergence detection"), 
/**Total comments extracted across all rounds*/
"total_comments": z.number().int().gte(0).describe("Total comments extracted across all rounds") }).describe("Emitted when meeting reaches convergence. Payload contains convergence metrics and stopping criteria.")
export type MeetingConvergedEvent = z.infer<typeof meetingConvergedEventSchema>

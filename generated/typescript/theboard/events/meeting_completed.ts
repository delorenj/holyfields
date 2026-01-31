import { z } from "zod"
import { baseEventSchema } from "../../base_event.js"

/**Emitted when meeting completes successfully. Payload contains final meeting state, metrics, and extracted insights (Phase 3A).*/
export const meetingCompletedEventSchema = baseEventSchema.extend({ 
/**Event type discriminator*/
"event_type": z.literal("meeting.completed").describe("Event type discriminator"), 
/**Total number of discussion rounds completed*/
"total_rounds": z.number().int().gte(1).describe("Total number of discussion rounds completed"), 
/**Total comments extracted across all rounds*/
"total_comments": z.number().int().gte(0).describe("Total comments extracted across all rounds"), 
/**Total cost in USD for all LLM calls*/
"total_cost": z.number().gte(0).describe("Total cost in USD for all LLM calls"), 
/**Whether convergence was detected before max_rounds*/
"convergence_detected": z.boolean().describe("Whether convergence was detected before max_rounds"), 
/**Reason the meeting stopped*/
"stopping_reason": z.enum(["convergence","max_rounds","manual"]).describe("Reason the meeting stopped"), 
/**Top 5 comments ranked by novelty score (Phase 3A insights)*/
"top_comments": z.array(z.any()).max(5).describe("Top 5 comments ranked by novelty score (Phase 3A insights)"), 
/**Distribution of comments by category (question, concern, idea, etc.)*/
"category_distribution": z.record(z.number().int().gte(0)).describe("Distribution of comments by category (question, concern, idea, etc.)"), 
/**Number of responses per agent*/
"agent_participation": z.record(z.number().int().gte(0)).describe("Number of responses per agent") }).describe("Emitted when meeting completes successfully. Payload contains final meeting state, metrics, and extracted insights (Phase 3A).")
export type MeetingCompletedEvent = z.infer<typeof meetingCompletedEventSchema>

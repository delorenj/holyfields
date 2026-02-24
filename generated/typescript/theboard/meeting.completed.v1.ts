import { z } from "zod"

/**Emitted when meeting completes successfully. Payload contains final meeting state, metrics, and extracted insights.*/
export const MeetingCompletedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("theboard.meeting.completed").describe("Event type discriminator"), "payload": z.object({ 
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
/**Top 5 comments ranked by novelty score*/
"top_comments": z.array(z.any()).max(5).describe("Top 5 comments ranked by novelty score"), 
/**Unique meeting identifier*/
"meeting_id": z.any().describe("Unique meeting identifier") }) }).and(z.intersection(z.any(), z.any())).describe("Emitted when meeting completes successfully. Payload contains final meeting state, metrics, and extracted insights.")
export type MeetingCompletedEvent = z.infer<typeof MeetingCompletedEventSchema>

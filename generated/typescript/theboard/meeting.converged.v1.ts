import { z } from "zod"

/**Emitted when meeting reaches convergence. Payload contains convergence metrics and stopping criteria.*/
export const MeetingConvergedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("theboard.meeting.converged").describe("Event type discriminator"), "payload": z.object({ 
/**Round number when convergence detected*/
"round_num": z.number().int().gte(1).describe("Round number when convergence detected"), 
/**Average novelty score that triggered convergence*/
"avg_novelty": z.number().gte(0).lte(1).describe("Average novelty score that triggered convergence"), 
/**Novelty threshold for convergence detection*/
"novelty_threshold": z.number().gte(0).lte(1).describe("Novelty threshold for convergence detection"), 
/**Total comments extracted across all rounds*/
"total_comments": z.number().int().gte(0).describe("Total comments extracted across all rounds"), 
/**Unique meeting identifier*/
"meeting_id": z.any().describe("Unique meeting identifier") }) }).and(z.intersection(z.any(), z.any())).describe("Emitted when meeting reaches convergence. Payload contains convergence metrics and stopping criteria.")
export type MeetingConvergedEvent = z.infer<typeof MeetingConvergedEventSchema>

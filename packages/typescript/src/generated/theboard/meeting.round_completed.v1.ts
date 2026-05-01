import { z } from "zod"

/**Emitted when a meeting round completes. Payload contains round metrics and convergence indicators.*/
export const TheboardMeetingRoundCompletedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("theboard.meeting.round_completed").describe("Event type discriminator"), "payload": z.object({ 
/**Round number that just completed*/
"round_num": z.number().int().gte(1).describe("Round number that just completed"), 
/**Name of agent who contributed in this round*/
"agent_name": z.any().describe("Name of agent who contributed in this round"), 
/**Character length of agent's response*/
"response_length": z.number().int().gte(0).describe("Character length of agent's response"), 
/**Number of comments extracted from response*/
"comment_count": z.number().int().gte(0).describe("Number of comments extracted from response"), 
/**Average novelty score of extracted comments (0.0 = repetitive, 1.0 = novel)*/
"avg_novelty": z.number().gte(0).lte(1).describe("Average novelty score of extracted comments (0.0 = repetitive, 1.0 = novel)"), 
/**Total tokens consumed (input + output)*/
"tokens_used": z.number().int().gte(0).describe("Total tokens consumed (input + output)"), 
/**Cost in USD for this round's LLM calls*/
"cost": z.number().gte(0).describe("Cost in USD for this round's LLM calls"), 
/**Unique meeting identifier*/
"meeting_id": z.any().describe("Unique meeting identifier") }) }).and(z.intersection(z.any(), z.any())).describe("Emitted when a meeting round completes. Payload contains round metrics and convergence indicators.")
export type TheboardMeetingRoundCompletedV1 = z.infer<typeof TheboardMeetingRoundCompletedV1Schema>

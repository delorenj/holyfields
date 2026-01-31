import { z } from "zod"
import { baseEventSchema } from "../../base_event.js"

/**Emitted when a meeting round completes. Payload contains round metrics and convergence indicators.*/
export const roundCompletedEventSchema = baseEventSchema.extend({ 
/**Event type discriminator*/
"event_type": z.literal("meeting.round_completed").describe("Event type discriminator"), 
/**Round number that just completed*/
"round_num": z.any().describe("Round number that just completed"), 
/**Name of agent who contributed in this round*/
"agent_name": z.any().describe("Name of agent who contributed in this round"), 
/**Character length of agent's response*/
"response_length": z.number().int().gte(0).describe("Character length of agent's response"), 
/**Number of comments extracted from response*/
"comment_count": z.number().int().gte(0).describe("Number of comments extracted from response"), 
/**Average novelty score of extracted comments*/
"avg_novelty": z.any().describe("Average novelty score of extracted comments"), 
/**Total tokens consumed (input + output)*/
"tokens_used": z.number().int().gte(0).describe("Total tokens consumed (input + output)"), 
/**Cost in USD for this round's LLM calls*/
"cost": z.number().gte(0).describe("Cost in USD for this round's LLM calls") }).describe("Emitted when a meeting round completes. Payload contains round metrics and convergence indicators.")
export type RoundCompletedEvent = z.infer<typeof roundCompletedEventSchema>

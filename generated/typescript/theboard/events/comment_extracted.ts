import { z } from "zod"
import { baseEventSchema } from "../../base_event.js"

/**Emitted when comments are extracted from agent response. Payload contains comment metadata for analytics.*/
export const commentExtractedEventSchema = baseEventSchema.extend({ 
/**Event type discriminator*/
"event_type": z.literal("meeting.comment_extracted").describe("Event type discriminator"), 
/**Round number when comment was extracted*/
"round_num": z.any().describe("Round number when comment was extracted"), 
/**Agent who authored the comment*/
"agent_name": z.any().describe("Agent who authored the comment"), 
/**Extracted comment text*/
"comment_text": z.string().min(1).max(5000).describe("Extracted comment text"), 
/**Comment category classified by notetaker agent*/
"category": z.enum(["question","concern","idea","observation","recommendation","clarification","other"]).describe("Comment category classified by notetaker agent"), 
/**Novelty score (0.0 = repetitive, 1.0 = novel)*/
"novelty_score": z.number().min(0.0).max(1.0).describe("Novelty score (0.0 = repetitive, 1.0 = novel)") }).describe("Emitted when comments are extracted from agent response. Payload contains comment metadata for analytics.")
export type CommentExtractedEvent = z.infer<typeof commentExtractedEventSchema>

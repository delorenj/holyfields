import { z } from "zod"

/**Emitted when comments are extracted from agent response. Payload contains comment metadata for analytics.*/
export const TheboardMeetingCommentExtractedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("theboard.meeting.comment_extracted").describe("Event type discriminator"), "payload": z.object({ 
/**Round number when comment was extracted*/
"round_num": z.number().int().gte(1).describe("Round number when comment was extracted"), 
/**Agent who authored the comment*/
"agent_name": z.any().describe("Agent who authored the comment"), 
/**Extracted comment text*/
"comment_text": z.string().min(1).max(5000).describe("Extracted comment text"), 
/**Comment category classified by notetaker agent*/
"category": z.enum(["technical_decision","risk","implementation_detail","observation","question","other"]).describe("Comment category classified by notetaker agent"), 
/**Novelty score (0.0 = repetitive, 1.0 = novel)*/
"novelty_score": z.number().gte(0).lte(1).describe("Novelty score (0.0 = repetitive, 1.0 = novel)"), 
/**Unique meeting identifier*/
"meeting_id": z.any().describe("Unique meeting identifier") }) }).and(z.intersection(z.any(), z.any())).describe("Emitted when comments are extracted from agent response. Payload contains comment metadata for analytics.")
export type TheboardMeetingCommentExtractedV1 = z.infer<typeof TheboardMeetingCommentExtractedV1Schema>

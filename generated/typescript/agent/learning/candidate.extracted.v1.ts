import { z } from "zod"

/**Candidate lesson extracted from repeated or high-signal episodes*/
export const CandidateExtractedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.learning.candidate.extracted").describe("Event type discriminator"), "payload": z.object({ 
/**Stable identifier for the candidate lesson*/
"candidate_id": z.any().describe("Stable identifier for the candidate lesson"), 
/**Operational lesson text proposed for validation*/
"rule_text": z.string().describe("Operational lesson text proposed for validation"), 
/**Episodes that justify the candidate lesson*/
"supporting_episode_ids": z.array(z.any()).describe("Episodes that justify the candidate lesson"), 
/**Skills or agent surfaces the lesson could apply to*/
"scope_skills": z.array(z.string()).describe("Skills or agent surfaces the lesson could apply to"), 
/**Tags used to decide when to retrieve this lesson*/
"trigger_tags": z.array(z.string()).describe("Tags used to decide when to retrieve this lesson").optional(), 
/**Promotion priority for the candidate lesson*/
"priority": z.enum(["low","medium","high","critical"]).describe("Promotion priority for the candidate lesson"), 
/**Why the candidate is worth validating*/
"rationale": z.union([z.string().describe("Why the candidate is worth validating"), z.null().describe("Why the candidate is worth validating")]).describe("Why the candidate is worth validating").optional() }) }).and(z.any()).describe("Candidate lesson extracted from repeated or high-signal episodes")
export type CandidateExtractedEvent = z.infer<typeof CandidateExtractedEventSchema>

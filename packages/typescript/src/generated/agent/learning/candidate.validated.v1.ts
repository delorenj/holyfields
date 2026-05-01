import { z } from "zod"

/**Validation result for a candidate lesson after replay and regression checks*/
export const AgentLearningCandidateValidatedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.learning.candidate.validated").describe("Event type discriminator"), "payload": z.object({ 
/**Candidate lesson being validated*/
"candidate_id": z.any().describe("Candidate lesson being validated"), 
/**Identifier for the eval or replay suite used during validation*/
"eval_suite": z.string().describe("Identifier for the eval or replay suite used during validation"), 
/**Outcome of candidate validation*/
"decision": z.enum(["promoted","rejected","needs_more_data"]).describe("Outcome of candidate validation"), 
/**Pass rate before applying the candidate rule*/
"replay_pass_rate_before": z.union([z.number().gte(0).lte(1).describe("Pass rate before applying the candidate rule"), z.null().describe("Pass rate before applying the candidate rule")]).describe("Pass rate before applying the candidate rule").optional(), 
/**Pass rate after applying the candidate rule*/
"replay_pass_rate_after": z.union([z.number().gte(0).lte(1).describe("Pass rate after applying the candidate rule"), z.null().describe("Pass rate after applying the candidate rule")]).describe("Pass rate after applying the candidate rule").optional(), 
/**Number of regression failures introduced by the candidate*/
"regression_failures": z.union([z.number().int().gte(0).describe("Number of regression failures introduced by the candidate"), z.null().describe("Number of regression failures introduced by the candidate")]).describe("Number of regression failures introduced by the candidate").optional(), 
/**Short explanation of why the candidate was promoted, rejected, or held*/
"notes": z.union([z.string().describe("Short explanation of why the candidate was promoted, rejected, or held"), z.null().describe("Short explanation of why the candidate was promoted, rejected, or held")]).describe("Short explanation of why the candidate was promoted, rejected, or held").optional() }) }).and(z.any()).describe("Validation result for a candidate lesson after replay and regression checks")
export type AgentLearningCandidateValidatedV1 = z.infer<typeof AgentLearningCandidateValidatedV1Schema>

import { z } from "zod"

/**Candidate lesson rejected after validation or review*/
export const AgentLearningLessonRejectedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.learning.lesson.rejected").describe("Event type discriminator"), "payload": z.object({ 
/**Candidate lesson that was rejected*/
"candidate_id": z.any().describe("Candidate lesson that was rejected"), 
/**Primary reason the candidate lesson was rejected*/
"rejection_reason": z.string().describe("Primary reason the candidate lesson was rejected"), 
/**Specific validation or review failures that blocked promotion*/
"blocking_failures": z.array(z.string()).describe("Specific validation or review failures that blocked promotion").optional() }) }).and(z.any()).describe("Candidate lesson rejected after validation or review")
export type AgentLearningLessonRejectedV1 = z.infer<typeof AgentLearningLessonRejectedV1Schema>

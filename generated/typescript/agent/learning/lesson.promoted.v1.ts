import { z } from "zod"

/**Validated lesson promoted into the active retrieval overlay*/
export const LessonPromotedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.learning.lesson.promoted").describe("Event type discriminator"), "payload": z.object({ 
/**Stable identifier for the active lesson*/
"lesson_id": z.any().describe("Stable identifier for the active lesson"), 
/**Candidate lesson that was promoted*/
"candidate_id": z.any().describe("Candidate lesson that was promoted"), 
/**Validated lesson text applied at runtime*/
"lesson_text": z.string().describe("Validated lesson text applied at runtime"), 
/**Skills or execution surfaces where the lesson should be retrieved*/
"scope_skills": z.array(z.string()).describe("Skills or execution surfaces where the lesson should be retrieved"), 
/**Tags used to match the lesson to future tasks*/
"trigger_tags": z.array(z.string()).describe("Tags used to match the lesson to future tasks").optional(), 
/**Whether the lesson is being observed or actively injected*/
"rollout_status": z.enum(["shadow","active"]).describe("Whether the lesson is being observed or actively injected"), 
/**Semantic version of the promoted lesson payload*/
"lesson_version": z.any().describe("Semantic version of the promoted lesson payload").optional(), 
/**Time-to-live before the lesson must be revalidated*/
"ttl_days": z.number().int().gte(1).describe("Time-to-live before the lesson must be revalidated") }) }).and(z.any()).describe("Validated lesson promoted into the active retrieval overlay")
export type LessonPromotedEvent = z.infer<typeof LessonPromotedEventSchema>

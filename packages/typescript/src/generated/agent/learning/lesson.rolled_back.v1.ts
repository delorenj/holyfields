import { z } from "zod"

/**Previously promoted lesson rolled back after poor runtime performance or operator review*/
export const AgentLearningLessonRolledBackV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.learning.lesson.rolled_back").describe("Event type discriminator"), "payload": z.object({ 
/**Active lesson being rolled back*/
"lesson_id": z.any().describe("Active lesson being rolled back"), 
/**Why the promoted lesson was disabled*/
"rollback_reason": z.string().describe("Why the promoted lesson was disabled"), 
/**Whether the rollback was partial or complete*/
"rollback_scope": z.enum(["partial","full"]).describe("Whether the rollback was partial or complete"), 
/**Replacement lesson id if a new lesson superseded the rollback*/
"replacement_lesson_id": z.union([z.string().describe("Replacement lesson id if a new lesson superseded the rollback"), z.null().describe("Replacement lesson id if a new lesson superseded the rollback")]).describe("Replacement lesson id if a new lesson superseded the rollback").optional() }) }).and(z.any()).describe("Previously promoted lesson rolled back after poor runtime performance or operator review")
export type AgentLearningLessonRolledBackV1 = z.infer<typeof AgentLearningLessonRolledBackV1Schema>

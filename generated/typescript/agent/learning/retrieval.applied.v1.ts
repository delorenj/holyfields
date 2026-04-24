import { z } from "zod"

/**Active lessons retrieved and applied to a live task or session*/
export const RetrievalAppliedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.learning.retrieval.applied").describe("Event type discriminator"), "payload": z.object({ 
/**Stable identifier for this retrieval application*/
"retrieval_id": z.any().describe("Stable identifier for this retrieval application"), 
/**Name of the agent receiving the retrieved lessons*/
"agent_name": z.any().describe("Name of the agent receiving the retrieved lessons"), 
/**Session identifier where the retrieval happened*/
"session_key": z.any().describe("Session identifier where the retrieval happened"), 
/**Promoted lessons injected into the live task context*/
"lesson_ids": z.array(z.any()).describe("Promoted lessons injected into the live task context"), 
/**Task tags used to select the active lessons*/
"task_tags": z.array(z.string()).describe("Task tags used to select the active lessons").optional(), 
/**Primary target skill or overlay consumer*/
"target_skill": z.union([z.string().describe("Primary target skill or overlay consumer"), z.null().describe("Primary target skill or overlay consumer")]).describe("Primary target skill or overlay consumer").optional() }) }).and(z.any()).describe("Active lessons retrieved and applied to a live task or session")
export type RetrievalAppliedEvent = z.infer<typeof RetrievalAppliedEventSchema>

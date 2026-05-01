import { z } from "zod"

/**Structured observation captured from agent execution for later episode synthesis*/
export const AgentLearningObservationRecordedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.learning.observation.recorded").describe("Event type discriminator"), "payload": z.object({ 
/**Stable identifier for the normalized observation*/
"observation_id": z.any().describe("Stable identifier for the normalized observation"), 
/**Name of the agent that produced the observation*/
"agent_name": z.any().describe("Name of the agent that produced the observation"), 
/**Session identifier associated with the observation*/
"session_key": z.any().describe("Session identifier associated with the observation"), 
/**Decision or checkpoint being observed (e.g. search_before_create, verification_step)*/
"decision_type": z.string().describe("Decision or checkpoint being observed (e.g. search_before_create, verification_step)"), 
/**Observed outcome of the decision*/
"outcome": z.enum(["success","failure","neutral"]).describe("Observed outcome of the decision"), 
/**Task tags used for later retrieval and grouping*/
"task_tags": z.array(z.string()).describe("Task tags used for later retrieval and grouping").optional(), 
/**Upstream event ids that justify the observation*/
"source_event_ids": z.array(z.any()).describe("Upstream event ids that justify the observation").optional(), 
/**Tool involved in the observation, if any*/
"tool_name": z.union([z.string().describe("Tool involved in the observation, if any"), z.null().describe("Tool involved in the observation, if any")]).describe("Tool involved in the observation, if any").optional(), 
/**Verification state at the time the observation was recorded*/
"verification_status": z.union([z.literal("not_run"), z.literal("passed"), z.literal("failed"), z.literal(null)]).describe("Verification state at the time the observation was recorded").optional(), 
/**Normalized failure class if the observation captured a miss*/
"failure_mode": z.union([z.string().describe("Normalized failure class if the observation captured a miss"), z.null().describe("Normalized failure class if the observation captured a miss")]).describe("Normalized failure class if the observation captured a miss").optional(), 
/**Brief summary of the corrective action taken*/
"fix_applied": z.union([z.string().describe("Brief summary of the corrective action taken"), z.null().describe("Brief summary of the corrective action taken")]).describe("Brief summary of the corrective action taken").optional(), 
/**Redacted short preview of relevant notes or evidence*/
"notes_preview": z.union([z.string().max(500).describe("Redacted short preview of relevant notes or evidence"), z.null().describe("Redacted short preview of relevant notes or evidence")]).describe("Redacted short preview of relevant notes or evidence").optional() }) }).and(z.any()).describe("Structured observation captured from agent execution for later episode synthesis")
export type AgentLearningObservationRecordedV1 = z.infer<typeof AgentLearningObservationRecordedV1Schema>

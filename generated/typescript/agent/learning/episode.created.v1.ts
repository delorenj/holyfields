import { z } from "zod"

/**Normalized episode synthesized from one or more learning observations*/
export const EpisodeCreatedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.learning.episode.created").describe("Event type discriminator"), "payload": z.object({ 
/**Stable identifier for the synthesized episode*/
"episode_id": z.any().describe("Stable identifier for the synthesized episode"), 
/**Name of the agent whose behavior produced the episode*/
"agent_name": z.any().describe("Name of the agent whose behavior produced the episode"), 
/**Session identifier associated with the episode*/
"session_key": z.any().describe("Session identifier associated with the episode"), 
/**Compact summary of what happened and why it mattered*/
"summary": z.string().describe("Compact summary of what happened and why it mattered"), 
/**Overall outcome of the episode*/
"outcome": z.enum(["success","failure","mixed"]).describe("Overall outcome of the episode"), 
/**Observation ids rolled up into this episode*/
"source_observation_ids": z.array(z.any()).describe("Observation ids rolled up into this episode"), 
/**Task tags carried forward for grouping and retrieval*/
"task_tags": z.array(z.string()).describe("Task tags carried forward for grouping and retrieval").optional(), 
/**Normalized failure class if the episode captured a miss*/
"failure_mode": z.union([z.string().describe("Normalized failure class if the episode captured a miss"), z.null().describe("Normalized failure class if the episode captured a miss")]).describe("Normalized failure class if the episode captured a miss").optional(), 
/**Summary of the fix or adjustment that improved the outcome*/
"fix_summary": z.union([z.string().describe("Summary of the fix or adjustment that improved the outcome"), z.null().describe("Summary of the fix or adjustment that improved the outcome")]).describe("Summary of the fix or adjustment that improved the outcome").optional(), 
/**Explicit user rating when available*/
"user_feedback_score": z.union([z.number().int().gte(1).lte(10).describe("Explicit user rating when available"), z.null().describe("Explicit user rating when available")]).describe("Explicit user rating when available").optional(), 
/**Redacted summary of explicit user feedback*/
"user_feedback_summary": z.union([z.string().describe("Redacted summary of explicit user feedback"), z.null().describe("Redacted summary of explicit user feedback")]).describe("Redacted summary of explicit user feedback").optional() }) }).and(z.any()).describe("Normalized episode synthesized from one or more learning observations")
export type EpisodeCreatedEvent = z.infer<typeof EpisodeCreatedEventSchema>

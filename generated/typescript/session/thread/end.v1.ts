import { z } from "zod"

/**Claude Code session ended*/
export const EndEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("session.thread.end").describe("Event type discriminator"), "payload": z.object({ "session_id": z.string(), "thread_id": z.union([z.string(), z.null()]).optional(), "end_reason": z.string(), "duration_seconds": z.union([z.number().int(), z.null()]).optional(), "total_turns": z.number().int().optional(), "total_tokens": z.union([z.number().int(), z.null()]).optional(), "total_cost_usd": z.union([z.number(), z.null()]).optional(), "tools_used": z.number().int().optional(), "files_modified": z.array(z.string()).optional(), "git_commits": z.array(z.string()).optional(), "final_status": z.string(), "summary": z.union([z.string(), z.null()]).optional(), "working_directory": z.union([z.string(), z.null()]).optional(), "git_branch": z.union([z.string(), z.null()]).optional() }) }).and(z.any()).describe("Claude Code session ended")
export type EndEvent = z.infer<typeof EndEventSchema>

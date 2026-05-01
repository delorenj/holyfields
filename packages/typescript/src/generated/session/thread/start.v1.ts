import { z } from "zod"

/**Claude Code session started*/
export const SessionThreadStartV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("session.thread.start").describe("Event type discriminator"), "payload": z.object({ "session_id": z.string(), "thread_id": z.union([z.string(), z.null()]).optional(), "working_directory": z.string(), "git_branch": z.union([z.string(), z.null()]).optional(), "git_remote": z.union([z.string(), z.null()]).optional(), "model": z.string(), "user_prompt": z.union([z.string(), z.null()]).optional(), "context_files": z.array(z.string()).optional(), "mcp_servers": z.array(z.string()).optional(), "started_at": z.string().optional() }) }).and(z.any()).describe("Claude Code session started")
export type SessionThreadStartV1 = z.infer<typeof SessionThreadStartV1Schema>

import { z } from "zod"

/**Claude Code tool was invoked*/
export const ActionEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("session.thread.agent.action").describe("Event type discriminator"), "payload": z.object({ "session_id": z.string(), "thread_id": z.union([z.string(), z.null()]).optional(), 
/**Name of the tool invoked*/
"tool_name": z.string().describe("Name of the tool invoked").optional(), 
/**Tool input parameters*/
"tool_input": z.record(z.string(), z.any()).describe("Tool input parameters").optional(), "working_directory": z.union([z.string(), z.null()]).optional(), "git_branch": z.union([z.string(), z.null()]).optional(), "files_in_context": z.array(z.string()).optional(), "turn_number": z.union([z.number().int(), z.null()]).optional(), "model": z.union([z.string(), z.null()]).optional(), "conversation_id": z.union([z.string(), z.null()]).optional(), 
/**Tool invocation metadata*/
"tool_metadata": z.record(z.string(), z.any()).describe("Tool invocation metadata"), "git_status": z.union([z.string(), z.null()]).optional(), "tags": z.array(z.string()).optional() }) }).and(z.any()).describe("Claude Code tool was invoked")
export type ActionEvent = z.infer<typeof ActionEventSchema>

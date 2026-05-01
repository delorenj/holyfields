import { z } from "zod"

/**Emitted when an agent session terminates. Carries summary statistics of the session (turn count, tool histogram, files touched, commits created) so consumers can build retrospective views without replaying every agent.tool.invoked event.*/
export const AgentSessionEndedV1Schema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("agent.session.ended").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("agent").describe("Locked domain for this schema.").optional(), 
/**Session-end payload with aggregate session statistics.*/
"data": z.object({ 
/**Identifier of the session that just ended. Matches the session_id from the corresponding agent.session.started event.*/
"session_id": z.any().describe("Identifier of the session that just ended. Matches the session_id from the corresponding agent.session.started event."), 
/**Why the session ended. user_stop: explicit termination. completed: agent finished its work. error: unrecoverable failure. timeout: idle/total budget exceeded. context_full: hit token limit.*/
"end_reason": z.enum(["user_stop","completed","error","timeout","context_full"]).describe("Why the session ended. user_stop: explicit termination. completed: agent finished its work. error: unrecoverable failure. timeout: idle/total budget exceeded. context_full: hit token limit."), 
/**Wall-clock seconds between session start and end.*/
"duration_seconds": z.number().int().gte(0).describe("Wall-clock seconds between session start and end."), 
/**Number of agent turns (tool invocations + responses) during the session.*/
"total_turns": z.number().int().gte(0).describe("Number of agent turns (tool invocations + responses) during the session."), 
/**Histogram mapping tool name to invocation count for the session.*/
"tools_used": z.record(z.number().int().gte(0)).describe("Histogram mapping tool name to invocation count for the session.").optional(), 
/**Repository-relative paths that were modified (uncommitted) at session end. Best-effort; reflects `git diff --name-only` at the moment the session ended.*/
"files_modified": z.array(z.string().min(1)).describe("Repository-relative paths that were modified (uncommitted) at session end. Best-effort; reflects `git diff --name-only` at the moment the session ended.").optional(), 
/**Commit SHAs created during the session, ordered most-recent first. Best-effort; reflects `git log --since=<started_at>` at the moment the session ended.*/
"git_commits": z.array(z.string().min(7).max(64)).describe("Commit SHAs created during the session, ordered most-recent first. Best-effort; reflects `git log --since=<started_at>` at the moment the session ended.").optional(), 
/**Outcome classifier. success: goals achieved. failure: blocked or aborted. partial: some goals met.*/
"final_status": z.enum(["success","failure","partial"]).describe("Outcome classifier. success: goals achieved. failure: blocked or aborted. partial: some goals met.").optional(), 
/**Absolute path the session ran in. Mirrors the value from agent.session.started.*/
"working_directory": z.string().min(1).describe("Absolute path the session ran in. Mirrors the value from agent.session.started.").optional(), 
/**Git branch at session end. May differ from session.started if the agent switched branches mid-session.*/
"git_branch": z.string().describe("Git branch at session end. May differ from session.started if the agent switched branches mid-session.").optional() }).strict().describe("Session-end payload with aggregate session statistics.") }).and(z.any()).describe("Emitted when an agent session terminates. Carries summary statistics of the session (turn count, tool histogram, files touched, commits created) so consumers can build retrospective views without replaying every agent.tool.invoked event.")
export type AgentSessionEndedV1 = z.infer<typeof AgentSessionEndedV1Schema>

import { z } from "zod"

/**Emitted when a subagent (a Task-tool spawned helper) finishes. Producer is the agent runtime (e.g. Claude Code via .claude/hooks/bloodbank-publisher.sh on SubagentStop). Distinct from agent.session.ended: the parent session continues; only the subagent has terminated. The session_id field points to the PARENT session so subagent activity rolls up under the originating session.*/
export const SubagentCompletedEventSchema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("agent.subagent.completed").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("agent").describe("Locked domain for this schema.").optional(), 
/**Subagent-completion payload.*/
"data": z.object({ 
/**Identifier of the PARENT session that spawned the subagent. Subagent activity rolls up under this session.*/
"session_id": z.any().describe("Identifier of the PARENT session that spawned the subagent. Subagent activity rolls up under this session."), 
/**Type/name of the subagent that finished (e.g. 'general-purpose', 'demo-architect'). Producer-defined; treat unknown values as opaque.*/
"agent_type": z.string().describe("Type/name of the subagent that finished (e.g. 'general-purpose', 'demo-architect'). Producer-defined; treat unknown values as opaque.").optional(), 
/**Why the subagent ended. completed: returned a result. error: unrecoverable failure. timeout: idle/total budget exceeded. user_stop: explicit termination.*/
"stop_reason": z.enum(["completed","error","timeout","user_stop"]).describe("Why the subagent ended. completed: returned a result. error: unrecoverable failure. timeout: idle/total budget exceeded. user_stop: explicit termination."), 
/**Absolute path the parent session was operating in when the subagent finished.*/
"working_directory": z.string().describe("Absolute path the parent session was operating in when the subagent finished.").optional() }).strict().describe("Subagent-completion payload.") }).and(z.any()).describe("Emitted when a subagent (a Task-tool spawned helper) finishes. Producer is the agent runtime (e.g. Claude Code via .claude/hooks/bloodbank-publisher.sh on SubagentStop). Distinct from agent.session.ended: the parent session continues; only the subagent has terminated. The session_id field points to the PARENT session so subagent activity rolls up under the originating session.")
export type SubagentCompletedEvent = z.infer<typeof SubagentCompletedEventSchema>

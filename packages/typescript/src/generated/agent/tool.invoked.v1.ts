import { z } from "zod"

/**Emitted when an agent invokes a tool. One event per invocation. Carries enough context (tool name, raw input, session, repo state) for downstream observability without persisting full conversation history. The tool_input field is opaque on purpose: each tool defines its own input shape and this schema does not constrain it.*/
export const AgentToolInvokedV1Schema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("agent.tool.invoked").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("agent").describe("Locked domain for this schema.").optional(), 
/**Tool-invocation payload.*/
"data": z.object({ 
/**Identifier of the session that issued this tool call. Matches session_id from the corresponding agent.session.started event.*/
"session_id": z.any().describe("Identifier of the session that issued this tool call. Matches session_id from the corresponding agent.session.started event."), 
/**Name of the tool the agent invoked (e.g., 'Bash', 'Read', 'Edit', 'Grep'). Producer-defined; consumers should treat unknown names as opaque rather than enum-restricted.*/
"tool_name": z.string().min(1).max(200).describe("Name of the tool the agent invoked (e.g., 'Bash', 'Read', 'Edit', 'Grep'). Producer-defined; consumers should treat unknown names as opaque rather than enum-restricted."), 
/**Raw tool-specific input as supplied by the agent. Schema is per-tool and intentionally not constrained here. Producers may redact or truncate at their discretion.*/
"tool_input": z.record(z.any()).describe("Raw tool-specific input as supplied by the agent. Schema is per-tool and intentionally not constrained here. Producers may redact or truncate at their discretion.").optional(), 
/**Absolute path the agent was operating in when the tool fired. Captured from session state, not re-evaluated per tool call.*/
"working_directory": z.string().describe("Absolute path the agent was operating in when the tool fired. Captured from session state, not re-evaluated per tool call.").optional(), 
/**Git branch at invocation time. Empty string when not in a git repo.*/
"git_branch": z.string().describe("Git branch at invocation time. Empty string when not in a git repo.").optional(), 
/**Coarse git working-tree state. clean: no uncommitted changes. modified: at least one tracked file diverges from HEAD.*/
"git_status": z.enum(["clean","modified"]).describe("Coarse git working-tree state. clean: no uncommitted changes. modified: at least one tracked file diverges from HEAD.").optional(), 
/**1-based turn counter within the session. Increments on every tool invocation.*/
"turn_number": z.number().int().gte(1).describe("1-based turn counter within the session. Increments on every tool invocation."), 
/**Producer's optimistic success flag at publish time. PostToolUse hooks fire AFTER the tool ran but cannot observe agent-level interpretation; treat false as authoritative, true as best-effort.*/
"success": z.boolean().describe("Producer's optimistic success flag at publish time. PostToolUse hooks fire AFTER the tool ran but cannot observe agent-level interpretation; treat false as authoritative, true as best-effort.").optional() }).strict().describe("Tool-invocation payload.") }).and(z.any()).describe("Emitted when an agent invokes a tool. One event per invocation. Carries enough context (tool name, raw input, session, repo state) for downstream observability without persisting full conversation history. The tool_input field is opaque on purpose: each tool defines its own input shape and this schema does not constrain it.")
export type AgentToolInvokedV1 = z.infer<typeof AgentToolInvokedV1Schema>

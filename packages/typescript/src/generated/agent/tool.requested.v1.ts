import { z } from "zod"

/**Emitted before an agent invokes a tool. Pairs with agent.tool.invoked: the request fires from the PreToolUse hook (intent), the invocation fires from the PostToolUse hook (result). Same session_id correlates them. Consumers use the pairing to detect tools that requested but never completed (cancellation, timeout, agent crash).*/
export const AgentToolRequestedV1Schema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("agent.tool.requested").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("agent").describe("Locked domain for this schema.").optional(), 
/**Tool-request payload (pre-execution).*/
"data": z.object({ 
/**Identifier of the session that issued the request. Matches session_id from the corresponding agent.session.started event.*/
"session_id": z.any().describe("Identifier of the session that issued the request. Matches session_id from the corresponding agent.session.started event."), 
/**Name of the tool the agent intends to invoke. Producer-defined; consumers should treat unknown names as opaque rather than enum-restricted.*/
"tool_name": z.string().min(1).max(200).describe("Name of the tool the agent intends to invoke. Producer-defined; consumers should treat unknown names as opaque rather than enum-restricted."), 
/**Raw tool-specific input as the agent prepared it. Schema is per-tool and intentionally not constrained here. Producers may redact or truncate at their discretion.*/
"tool_input": z.record(z.any()).describe("Raw tool-specific input as the agent prepared it. Schema is per-tool and intentionally not constrained here. Producers may redact or truncate at their discretion.").optional(), 
/**Absolute path the agent was operating in when the request was made.*/
"working_directory": z.string().describe("Absolute path the agent was operating in when the request was made.").optional(), 
/**Git branch at request time. Empty string when not in a git repo.*/
"git_branch": z.string().describe("Git branch at request time. Empty string when not in a git repo.").optional(), 
/**1-based turn counter within the session at the time of the request.*/
"turn_number": z.number().int().gte(1).describe("1-based turn counter within the session at the time of the request.") }).strict().describe("Tool-request payload (pre-execution).") }).and(z.any()).describe("Emitted before an agent invokes a tool. Pairs with agent.tool.invoked: the request fires from the PreToolUse hook (intent), the invocation fires from the PostToolUse hook (result). Same session_id correlates them. Consumers use the pairing to detect tools that requested but never completed (cancellation, timeout, agent crash).")
export type AgentToolRequestedV1 = z.infer<typeof AgentToolRequestedV1Schema>

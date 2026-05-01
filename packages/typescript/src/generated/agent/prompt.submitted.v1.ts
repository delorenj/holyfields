import { z } from "zod"

/**Emitted when a user submits a prompt to an agent. Producer is the agent runtime (e.g. Claude Code via .claude/hooks/bloodbank-publisher.sh on UserPromptSubmit). Carries the raw prompt text alongside repo state at submission time. Consumers use it to attribute downstream tool invocations to a user intent and to build retrospective views of what was asked.*/
export const AgentPromptSubmittedV1Schema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("agent.prompt.submitted").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("agent").describe("Locked domain for this schema.").optional(), 
/**Prompt-submission payload.*/
"data": z.object({ 
/**Identifier of the session the prompt belongs to. Matches the session_id from the corresponding agent.session.started event.*/
"session_id": z.any().describe("Identifier of the session the prompt belongs to. Matches the session_id from the corresponding agent.session.started event."), 
/**Raw prompt text as submitted by the user. May be truncated by the producer at its discretion; see prompt_length for the original size before any truncation.*/
"prompt_text": z.string().describe("Raw prompt text as submitted by the user. May be truncated by the producer at its discretion; see prompt_length for the original size before any truncation."), 
/**Character length of the original prompt before any truncation. Lets consumers detect truncation by comparing against `len(prompt_text)`.*/
"prompt_length": z.number().int().gte(0).describe("Character length of the original prompt before any truncation. Lets consumers detect truncation by comparing against `len(prompt_text)`."), 
/**Absolute path the agent is operating in at prompt-submit time.*/
"working_directory": z.string().describe("Absolute path the agent is operating in at prompt-submit time.").optional(), 
/**Git branch at prompt-submit time. Empty string when not in a git repo.*/
"git_branch": z.string().describe("Git branch at prompt-submit time. Empty string when not in a git repo.").optional() }).strict().describe("Prompt-submission payload.") }).and(z.any()).describe("Emitted when a user submits a prompt to an agent. Producer is the agent runtime (e.g. Claude Code via .claude/hooks/bloodbank-publisher.sh on UserPromptSubmit). Carries the raw prompt text alongside repo state at submission time. Consumers use it to attribute downstream tool invocations to a user intent and to build retrospective views of what was asked.")
export type AgentPromptSubmittedV1 = z.infer<typeof AgentPromptSubmittedV1Schema>

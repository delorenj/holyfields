import { z } from "zod"

/**Emitted when an agent session begins. Producer is typically the agent runtime itself (e.g., Claude Code via .claude/hooks/bloodbank-publisher.sh on SessionStart). Consumers track session lifecycle, attribute downstream events to a session, and aggregate per-session metrics.*/
export const SessionStartedEventSchema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("agent.session.started").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("agent").describe("Locked domain for this schema.").optional(), 
/**Session-start payload.*/
"data": z.object({ 
/**Stable identifier for this session. Used as the correlation key for all downstream agent.* events from the same session.*/
"session_id": z.any().describe("Stable identifier for this session. Used as the correlation key for all downstream agent.* events from the same session."), 
/**Absolute path the agent is operating in at session start. Captured once; subsequent cd within tools is not reflected here.*/
"working_directory": z.string().min(1).describe("Absolute path the agent is operating in at session start. Captured once; subsequent cd within tools is not reflected here."), 
/**Git branch the agent is on at session start. Empty string when not in a git repo.*/
"git_branch": z.string().describe("Git branch the agent is on at session start. Empty string when not in a git repo.").optional(), 
/**Origin remote URL for the working_directory's repo. Empty string when not in a git repo or when no origin is configured.*/
"git_remote": z.string().describe("Origin remote URL for the working_directory's repo. Empty string when not in a git repo or when no origin is configured.").optional(), 
/**RFC3339 UTC timestamp at which the session began. Producers should set this to match the envelope `time` field.*/
"started_at": z.any().describe("RFC3339 UTC timestamp at which the session began. Producers should set this to match the envelope `time` field.") }).strict().describe("Session-start payload.") }).and(z.any()).describe("Emitted when an agent session begins. Producer is typically the agent runtime itself (e.g., Claude Code via .claude/hooks/bloodbank-publisher.sh on SessionStart). Consumers track session lifecycle, attribute downstream events to a session, and aggregate per-session metrics.")
export type SessionStartedEvent = z.infer<typeof SessionStartedEventSchema>

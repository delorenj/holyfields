import { z } from "zod"

/**Agent invoked a tool (exec, web_search, read, etc.)*/
export const ToolInvokedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.tool.invoked").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the agent invoking the tool*/
"agent_name": z.any().describe("Name of the agent invoking the tool"), 
/**Name of the tool (e.g., 'exec', 'web_search', 'read')*/
"tool_name": z.string().describe("Name of the tool (e.g., 'exec', 'web_search', 'read')"), 
/**First 200 characters of tool parameters*/
"tool_params_preview": z.string().max(200).describe("First 200 characters of tool parameters"), 
/**Session identifier*/
"session_key": z.any().describe("Session identifier") }) }).and(z.any()).describe("Agent invoked a tool (exec, web_search, read, etc.)")
export type ToolInvokedEvent = z.infer<typeof ToolInvokedEventSchema>

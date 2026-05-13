import { z } from "zod"

/**Emitted when the GitHub Copilot CLI agent loop stops. Producer is bloodbank/services/agent-hooks/copilot/publish.py invoked via the agentStop hook. The data.payload field is a passthrough of the Copilot-supplied hook JSON; treat as opaque.*/
export const CopilotAgentStoppedV1Schema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("copilot.agent.stopped").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("copilot").describe("Locked domain for this schema.").optional(), 
/**Copilot agent-stop payload.*/
"data": z.object({ 
/**Locked Copilot hook name for this schema.*/
"hook": z.literal("agentStop").describe("Locked Copilot hook name for this schema."), 
/**Raw stdin JSON the Copilot CLI supplied to the hook. Schema is owned by Copilot upstream and is intentionally not constrained here.*/
"payload": z.record(z.any()).describe("Raw stdin JSON the Copilot CLI supplied to the hook. Schema is owned by Copilot upstream and is intentionally not constrained here.") }).strict().describe("Copilot agent-stop payload.") }).and(z.any()).describe("Emitted when the GitHub Copilot CLI agent loop stops. Producer is bloodbank/services/agent-hooks/copilot/publish.py invoked via the agentStop hook. The data.payload field is a passthrough of the Copilot-supplied hook JSON; treat as opaque.")
export type CopilotAgentStoppedV1 = z.infer<typeof CopilotAgentStoppedV1Schema>

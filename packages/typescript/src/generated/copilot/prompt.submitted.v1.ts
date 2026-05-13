import { z } from "zod"

/**Emitted when a user prompt is submitted to GitHub Copilot CLI. Producer is bloodbank/services/agent-hooks/copilot/publish.py invoked via the userPromptSubmitted hook. The data.payload field is a passthrough of the Copilot-supplied hook JSON; treat as opaque.*/
export const CopilotPromptSubmittedV1Schema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("copilot.prompt.submitted").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("copilot").describe("Locked domain for this schema.").optional(), 
/**Copilot prompt-submission payload.*/
"data": z.object({ 
/**Locked Copilot hook name for this schema.*/
"hook": z.literal("userPromptSubmitted").describe("Locked Copilot hook name for this schema."), 
/**Raw stdin JSON the Copilot CLI supplied to the hook. Schema is owned by Copilot upstream and is intentionally not constrained here.*/
"payload": z.record(z.any()).describe("Raw stdin JSON the Copilot CLI supplied to the hook. Schema is owned by Copilot upstream and is intentionally not constrained here.") }).strict().describe("Copilot prompt-submission payload.") }).and(z.any()).describe("Emitted when a user prompt is submitted to GitHub Copilot CLI. Producer is bloodbank/services/agent-hooks/copilot/publish.py invoked via the userPromptSubmitted hook. The data.payload field is a passthrough of the Copilot-supplied hook JSON; treat as opaque.")
export type CopilotPromptSubmittedV1 = z.infer<typeof CopilotPromptSubmittedV1Schema>

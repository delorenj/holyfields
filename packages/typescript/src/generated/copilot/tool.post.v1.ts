import { z } from "zod"

/**Emitted after a GitHub Copilot CLI tool runs. Producer is bloodbank/services/agent-hooks/copilot/publish.py invoked via the postToolUse hook. The data.payload field is a passthrough of the Copilot-supplied hook JSON; treat as opaque.*/
export const CopilotToolPostV1Schema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("copilot.tool.post").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("copilot").describe("Locked domain for this schema.").optional(), 
/**Copilot post-tool-use payload.*/
"data": z.object({ 
/**Locked Copilot hook name for this schema.*/
"hook": z.literal("postToolUse").describe("Locked Copilot hook name for this schema."), 
/**Raw stdin JSON the Copilot CLI supplied to the hook. Schema is owned by Copilot upstream and is intentionally not constrained here.*/
"payload": z.record(z.any()).describe("Raw stdin JSON the Copilot CLI supplied to the hook. Schema is owned by Copilot upstream and is intentionally not constrained here.") }).strict().describe("Copilot post-tool-use payload.") }).and(z.any()).describe("Emitted after a GitHub Copilot CLI tool runs. Producer is bloodbank/services/agent-hooks/copilot/publish.py invoked via the postToolUse hook. The data.payload field is a passthrough of the Copilot-supplied hook JSON; treat as opaque.")
export type CopilotToolPostV1 = z.infer<typeof CopilotToolPostV1Schema>

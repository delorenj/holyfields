import { z } from "zod"

/**Emitted when GitHub Copilot CLI encounters an error. Producer is bloodbank/services/agent-hooks/copilot/publish.py invoked via the errorOccurred hook. The data.payload field is a passthrough of the Copilot-supplied hook JSON; treat as opaque.*/
export const CopilotErrorOccurredV1Schema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("copilot.error.occurred").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("copilot").describe("Locked domain for this schema.").optional(), 
/**Copilot error payload.*/
"data": z.object({ 
/**Locked Copilot hook name for this schema.*/
"hook": z.literal("errorOccurred").describe("Locked Copilot hook name for this schema."), 
/**Raw stdin JSON the Copilot CLI supplied to the hook. Schema is owned by Copilot upstream and is intentionally not constrained here.*/
"payload": z.record(z.any()).describe("Raw stdin JSON the Copilot CLI supplied to the hook. Schema is owned by Copilot upstream and is intentionally not constrained here.") }).strict().describe("Copilot error payload.") }).and(z.any()).describe("Emitted when GitHub Copilot CLI encounters an error. Producer is bloodbank/services/agent-hooks/copilot/publish.py invoked via the errorOccurred hook. The data.payload field is a passthrough of the Copilot-supplied hook JSON; treat as opaque.")
export type CopilotErrorOccurredV1 = z.infer<typeof CopilotErrorOccurredV1Schema>

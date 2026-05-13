import { z } from "zod"

/**Emitted when a GitHub Copilot CLI session begins. Producer is bloodbank/services/agent-hooks/copilot/publish.py invoked via ~/.copilot/hooks/bloodbank.json on the sessionStart hook. The data.payload field is a passthrough of the Copilot-supplied hook JSON; treat as opaque.*/
export const CopilotSessionStartedV1Schema = z.object({ 
/**Locked event type for this schema.*/
"type": z.literal("copilot.session.started").describe("Locked event type for this schema.").optional(), 
/**Locked domain for this schema.*/
"domain": z.literal("copilot").describe("Locked domain for this schema.").optional(), 
/**Copilot session-start payload.*/
"data": z.object({ 
/**Locked Copilot hook name for this schema.*/
"hook": z.literal("sessionStart").describe("Locked Copilot hook name for this schema."), 
/**Raw stdin JSON the Copilot CLI supplied to the hook. Schema is owned by Copilot upstream and is intentionally not constrained here.*/
"payload": z.record(z.any()).describe("Raw stdin JSON the Copilot CLI supplied to the hook. Schema is owned by Copilot upstream and is intentionally not constrained here.") }).strict().describe("Copilot session-start payload.") }).and(z.any()).describe("Emitted when a GitHub Copilot CLI session begins. Producer is bloodbank/services/agent-hooks/copilot/publish.py invoked via ~/.copilot/hooks/bloodbank.json on the sessionStart hook. The data.payload field is a passthrough of the Copilot-supplied hook JSON; treat as opaque.")
export type CopilotSessionStartedV1 = z.infer<typeof CopilotSessionStartedV1Schema>

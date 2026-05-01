import { z } from "zod"

/**Extension schema for TheBoard events. Adds meeting_id field for meeting correlation. Use with allOf to extend base_event.*/
export const CommonTheboardExtensionV1Schema = z.object({ 
/**UUID of the meeting this event relates to. Used for event correlation and tracing within TheBoard domain.*/
"meeting_id": z.any().describe("UUID of the meeting this event relates to. Used for event correlation and tracing within TheBoard domain.") }).describe("Extension schema for TheBoard events. Adds meeting_id field for meeting correlation. Use with allOf to extend base_event.")
export type CommonTheboardExtensionV1 = z.infer<typeof CommonTheboardExtensionV1Schema>

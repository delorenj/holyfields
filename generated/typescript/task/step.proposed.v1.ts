import { z } from "zod"

/**Emitted when a working step is proposed*/
export const StepProposedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("task.step.proposed").describe("Event type discriminator"), "payload": z.object({ 
/**UUID of the task*/
"task_id": z.any().describe("UUID of the task"), 
/**Ticket or Issue ID (e.g. TICKET-101)*/
"ticket_id": z.string().describe("Ticket or Issue ID (e.g. TICKET-101)"), "changeset": z.object({ 
/**File path*/
"file": z.string().describe("File path"), 
/**Proposed diff*/
"diff": z.string().describe("Proposed diff") }), 
/**Command or plan to validate this change (e.g. npm test)*/
"validation_plan": z.string().describe("Command or plan to validate this change (e.g. npm test)").optional() }) }).and(z.any()).describe("Emitted when a working step is proposed")
export type StepProposedEvent = z.infer<typeof StepProposedEventSchema>

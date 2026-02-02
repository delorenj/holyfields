import { z } from "zod"

/**Emitted when a working step is proposed*/
export const taskStepProposedEventSchema = z.object({ "event_type": z.literal("task.step.proposed"), "timestamp": z.any(), "task_id": z.any(), 
/**Ticket or Issue ID (e.g. TICKET-101)*/
"ticket_id": z.string().describe("Ticket or Issue ID (e.g. TICKET-101)"), "changeset": z.object({ "file": z.string(), "diff": z.string() }), 
/**Command or plan to validate this change (e.g. npm test)*/
"validation_plan": z.string().describe("Command or plan to validate this change (e.g. npm test)").optional() }).describe("Emitted when a working step is proposed")
export type TaskStepProposedEvent = z.infer<typeof taskStepProposedEventSchema>

import { z } from "zod"

/**External task routed to an agent*/
export const TaskAssignedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("agent.task.assigned").describe("Event type discriminator"), "payload": z.object({ 
/**Name of the agent the task is assigned to*/
"agent_name": z.any().describe("Name of the agent the task is assigned to"), 
/**Who assigned the task (e.g., 'plane', 'cack', 'jarad')*/
"source": z.string().describe("Who assigned the task (e.g., 'plane', 'cack', 'jarad')"), 
/**Type of task*/
"task_type": z.enum(["ticket","message","cron","adhoc"]).describe("Type of task"), 
/**First 200 characters of the task description*/
"task_preview": z.string().max(200).describe("First 200 characters of the task description") }) }).and(z.any()).describe("External task routed to an agent")
export type TaskAssignedEvent = z.infer<typeof TaskAssignedEventSchema>

import { z } from "zod"

/**Emitted when a working step is executed and validated*/
export const StepExecutedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("task.step.executed").describe("Event type discriminator"), "payload": z.object({ 
/**UUID of the task*/
"task_id": z.any().describe("UUID of the task"), 
/**UUID of this step*/
"step_id": z.any().describe("UUID of this step").optional(), 
/**Path to the file that was modified*/
"file_path": z.string().describe("Path to the file that was modified").optional(), 
/**Git diff of the changes*/
"diff": z.string().describe("Git diff of the changes").optional(), 
/**Result of test execution*/
"test_result": z.enum(["passed","failed","skipped"]).describe("Result of test execution"), 
/**Human review status*/
"approval_status": z.enum(["approved","rejected","pending"]).describe("Human review status") }) }).and(z.any()).describe("Emitted when a working step is executed and validated")
export type StepExecutedEvent = z.infer<typeof StepExecutedEventSchema>

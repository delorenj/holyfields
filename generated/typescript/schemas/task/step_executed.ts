import { z } from "zod"

/**Emitted when a working step is executed and validated*/
export const taskStepExecutedEventSchema = z.object({ "event_type": z.literal("task.step.executed"), "timestamp": z.any(), "task_id": z.any(), "step_id": z.any().optional(), "file_path": z.string().optional(), "diff": z.string().optional(), "test_result": z.enum(["passed","failed","skipped"]), "approval_status": z.enum(["approved","rejected","pending"]) }).describe("Emitted when a working step is executed and validated")
export type TaskStepExecutedEvent = z.infer<typeof taskStepExecutedEventSchema>

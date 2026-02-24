import { z } from "zod"

/**Transcription or processing failed*/
export const FailedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("fireflies.transcript.failed").describe("Event type discriminator"), "payload": z.object({ 
/**Stage that failed*/
"failed_stage": z.enum(["upload","transcription","processing"]).describe("Stage that failed"), 
/**Error message*/
"error_message": z.string().describe("Error message"), 
/**Error code*/
"error_code": z.union([z.string().describe("Error code"), z.null().describe("Error code")]).describe("Error code").optional(), 
/**Transcript ID if available*/
"transcript_id": z.union([z.string().describe("Transcript ID if available"), z.null().describe("Transcript ID if available")]).describe("Transcript ID if available").optional(), 
/**Original file path*/
"media_file": z.union([z.string().describe("Original file path"), z.null().describe("Original file path")]).describe("Original file path").optional(), 
/**Retry attempts*/
"retry_count": z.number().int().gte(0).describe("Retry attempts").optional(), 
/**Whether error is retryable*/
"is_retryable": z.boolean().describe("Whether error is retryable").optional() }) }).and(z.any()).describe("Transcription or processing failed")
export type FailedEvent = z.infer<typeof FailedEventSchema>

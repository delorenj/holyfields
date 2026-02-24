import { z } from "zod"

/**Request to upload media to Fireflies for transcription*/
export const UploadEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("fireflies.transcript.upload").describe("Event type discriminator"), "payload": z.object({ 
/**Path or URL to media file*/
"media_file": z.string().describe("Path or URL to media file"), 
/**Duration of media in seconds*/
"media_duration_seconds": z.number().int().gte(1).describe("Duration of media in seconds"), 
/**MIME type (e.g., 'audio/mpeg', 'video/mp4')*/
"media_type": z.string().describe("MIME type (e.g., 'audio/mpeg', 'video/mp4')"), 
/**Meeting title*/
"title": z.union([z.string().describe("Meeting title"), z.null().describe("Meeting title")]).describe("Meeting title").optional(), 
/**User requesting transcription*/
"user_id": z.union([z.string().describe("User requesting transcription"), z.null().describe("User requesting transcription")]).describe("User requesting transcription").optional() }) }).and(z.any()).describe("Request to upload media to Fireflies for transcription")
export type UploadEvent = z.infer<typeof UploadEventSchema>

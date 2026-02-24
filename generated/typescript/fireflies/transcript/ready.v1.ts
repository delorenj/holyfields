import { z } from "zod"

/**Fireflies completed transcription*/
export const ReadyEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("fireflies.transcript.ready").describe("Event type discriminator"), "payload": z.object({ 
/**Fireflies meeting/transcript ID*/
"transcript_id": z.string().describe("Fireflies meeting/transcript ID"), 
/**Meeting title*/
"title": z.string().describe("Meeting title"), 
/**Meeting date/time*/
"date": z.string().datetime({ offset: true }).describe("Meeting date/time"), 
/**Duration in minutes*/
"duration_minutes": z.number().gte(0).describe("Duration in minutes"), 
/**URL to transcript*/
"transcript_url": z.string().url().describe("URL to transcript"), 
/**URL to audio if available*/
"audio_url": z.union([z.string().url().describe("URL to audio if available"), z.null().describe("URL to audio if available")]).describe("URL to audio if available").optional(), 
/**URL to video if available*/
"video_url": z.union([z.string().url().describe("URL to video if available"), z.null().describe("URL to video if available")]).describe("URL to video if available").optional(), 
/**Transcript sentences*/
"sentences": z.array(z.any()).describe("Transcript sentences"), 
/**Meeting summary if generated*/
"summary": z.union([z.string().describe("Meeting summary if generated"), z.null().describe("Meeting summary if generated")]).describe("Meeting summary if generated").optional(), "participants": z.array(z.object({ "name": z.string(), "email": z.union([z.string().email(), z.null()]).optional() })).optional() }) }).and(z.any()).describe("Fireflies completed transcription")
export type ReadyEvent = z.infer<typeof ReadyEventSchema>

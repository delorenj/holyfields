import { z } from "zod"

/**Base schema for all voice-related events across the Hey-Ma ecosystem. Provides common fields for transcription, audio metadata, and session tracking. All voice component events extend this base.*/
export const baseVoiceEventSchema = z.object({ 
/**Event discriminator for routing (e.g., 'whisperlivekit.transcription.completed'). Used by Bloodbank for topic-based routing.*/
"event_type": z.string().regex(new RegExp("^[a-z0-9]+\\.[a-z0-9._]+$")).describe("Event discriminator for routing (e.g., 'whisperlivekit.transcription.completed'). Used by Bloodbank for topic-based routing."), 
/**ISO 8601 UTC timestamp when event was emitted*/
"timestamp": z.any().describe("ISO 8601 UTC timestamp when event was emitted"), 
/**UUID of the voice session this event relates to. Used for event correlation and tracing across the voice-to-response pipeline.*/
"session_id": z.any().describe("UUID of the voice session this event relates to. Used for event correlation and tracing across the voice-to-response pipeline."), 
/**Component that emitted this event (e.g., 'whisperlivekit', 'tonny', 'candybar')*/
"source": z.string().regex(new RegExp("^[a-z0-9_-]+$")).describe("Component that emitted this event (e.g., 'whisperlivekit', 'tonny', 'candybar')"), 
/**Intended consumer of this event (e.g., 'tonny', 'candybar'). Used for targeted routing.*/
"target": z.string().regex(new RegExp("^[a-z0-9_-]+$")).describe("Intended consumer of this event (e.g., 'tonny', 'candybar'). Used for targeted routing.") }).describe("Base schema for all voice-related events across the Hey-Ma ecosystem. Provides common fields for transcription, audio metadata, and session tracking. All voice component events extend this base.")
export type BaseVoiceEvent = z.infer<typeof baseVoiceEventSchema>

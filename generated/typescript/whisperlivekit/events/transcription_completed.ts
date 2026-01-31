import { z } from "zod"
import { baseVoiceEventSchema } from '../../base_voice_event';

/**Metadata about the audio that was transcribed*/
const audioMetadataSchema = z.object({
  /**Duration of the audio segment in milliseconds*/
  duration_ms: z.number().int().gte(0).describe("Duration of the audio segment in milliseconds"),
  /**Audio sample rate in Hz (e.g., 16000)*/
  sample_rate: z.number().int().gte(8000).lte(48000).describe("Audio sample rate in Hz (e.g., 16000)"),
  /**Number of audio channels (1=mono, 2=stereo)*/
  channels: z.number().int().gte(1).lte(2).describe("Number of audio channels (1=mono, 2=stereo)"),
  /**Audio bit depth*/
  bit_depth: z.union([z.literal(8), z.literal(16), z.literal(24), z.literal(32)]).describe("Audio bit depth").optional(),
  /**Audio format*/
  format: z.enum(["pcm","wav","mp3","opus"]).describe("Audio format"),
  /**Detected or specified language code (ISO 639-1, e.g., 'en', 'es')*/
  language: z.union([z.string().regex(new RegExp("^[a-z]{2}$")).describe("Detected or specified language code (ISO 639-1, e.g., 'en', 'es')"), z.null().describe("Detected or specified language code (ISO 639-1, e.g., 'en', 'es')")]).describe("Detected or specified language code (ISO 639-1, e.g., 'en', 'es')").optional(),
  /**Transcription confidence score (0.0 to 1.0)*/
  confidence: z.union([z.number().gte(0).lte(1).describe("Transcription confidence score (0.0 to 1.0)"), z.null().describe("Transcription confidence score (0.0 to 1.0)")]).describe("Transcription confidence score (0.0 to 1.0)").optional()
}).catchall(z.any()).describe("Metadata about the audio that was transcribed");

/**Emitted when WhisperLiveKit completes transcription of an audio segment. This event triggers the voice-to-response pipeline by notifying Tonny agent and other consumers.*/
export const transcriptionCompletedEventSchema = baseVoiceEventSchema.extend({
  /**Event type discriminator*/
  event_type: z.literal("whisperlivekit.transcription.completed").describe("Event type discriminator"),
  /**Transcribed text from the audio segment*/
  text: z.string().min(1).max(10000).describe("Transcribed text from the audio segment"),
  /**Metadata about the audio that was transcribed*/
  audio_metadata: audioMetadataSchema,
  /**Whether this is a final transcription (true) or partial/streaming result (false)*/
  is_final: z.boolean().describe("Whether this is a final transcription (true) or partial/streaming result (false)").default(true),
  /**Unique identifier for this audio segment within the session*/
  segment_id: z.union([z.string().describe("Unique identifier for this audio segment within the session"), z.null().describe("Unique identifier for this audio segment within the session")]).describe("Unique identifier for this audio segment within the session").optional()
}).strict().describe("Emitted when WhisperLiveKit completes transcription of an audio segment. This event triggers the voice-to-response pipeline by notifying Tonny agent and other consumers.");

export type TranscriptionCompletedEvent = z.infer<typeof transcriptionCompletedEventSchema>;

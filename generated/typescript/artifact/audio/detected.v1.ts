import { z } from "zod"

/**Audio file detected in the audio inbox and ready for downstream workflow processing*/
export const DetectedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("artifact.audio.detected").describe("Event type discriminator"), "payload": z.object({ 
/**Human-readable logical source where file was detected*/
"inbox_source": z.literal("audio inbox").describe("Human-readable logical source where file was detected"), 
/**Detected file name*/
"file_name": z.string().min(1).describe("Detected file name"), 
/**Absolute or relative file path as seen by the detector*/
"file_path": z.string().min(1).describe("Absolute or relative file path as seen by the detector"), 
/**Lowercase extension without dot (e.g. 'mp3', 'wav', 'm4a', 'ogg')*/
"file_extension": z.string().regex(new RegExp("^[a-z0-9]+$")).describe("Lowercase extension without dot (e.g. 'mp3', 'wav', 'm4a', 'ogg')"), 
/**Detected MIME type if known*/
"mime_type": z.union([z.string().describe("Detected MIME type if known"), z.null().describe("Detected MIME type if known")]).describe("Detected MIME type if known").optional(), 
/**File size in bytes if known*/
"file_size_bytes": z.union([z.number().int().gte(0).describe("File size in bytes if known"), z.null().describe("File size in bytes if known")]).describe("File size in bytes if known").optional(), 
/**Timestamp when detector noticed the file*/
"detected_at": z.any().describe("Timestamp when detector noticed the file"), 
/**Detector identity (e.g. 'node-red-flow-orchestrator')*/
"detector": z.union([z.string().describe("Detector identity (e.g. 'node-red-flow-orchestrator')"), z.null().describe("Detector identity (e.g. 'node-red-flow-orchestrator')")]).describe("Detector identity (e.g. 'node-red-flow-orchestrator')").optional(), 
/**Optional content hash for dedupe/correlation*/
"sha256": z.union([z.string().regex(new RegExp("^[a-f0-9]{64}$")).describe("Optional content hash for dedupe/correlation"), z.null().describe("Optional content hash for dedupe/correlation")]).describe("Optional content hash for dedupe/correlation").optional(), 
/**Additional source-specific metadata*/
"metadata": z.record(z.any()).describe("Additional source-specific metadata").optional() }) }).and(z.any()).describe("Audio file detected in the audio inbox and ready for downstream workflow processing")
export type DetectedEvent = z.infer<typeof DetectedEventSchema>

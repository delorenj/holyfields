import { z } from "zod"

/**Artifact was created, updated, or deleted*/
export const LifecycleEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.enum(["artifact.created","artifact.updated","artifact.deleted"]).describe("Event type discriminator"), "payload": z.object({ 
/**Lifecycle action*/
"action": z.enum(["created","updated","deleted"]).describe("Lifecycle action"), 
/**Type of artifact*/
"kind": z.enum(["transcript","code","document","image","audio"]).describe("Type of artifact"), 
/**File path or URL*/
"uri": z.string().url().describe("File path or URL"), 
/**Artifact title*/
"title": z.union([z.string().describe("Artifact title"), z.null().describe("Artifact title")]).describe("Artifact title").optional(), 
/**Full content if applicable*/
"content": z.union([z.string().describe("Full content if applicable"), z.null().describe("Full content if applicable")]).describe("Full content if applicable").optional(), 
/**Additional metadata*/
"metadata": z.record(z.string(), z.any()).describe("Additional metadata").optional() }) }).and(z.any()).describe("Artifact was created, updated, or deleted")
export type LifecycleEvent = z.infer<typeof LifecycleEventSchema>

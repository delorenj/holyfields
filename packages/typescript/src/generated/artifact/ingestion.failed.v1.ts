import { z } from "zod"

/**Artifact ingestion into RAG failed*/
export const ArtifactIngestionFailedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("artifact.ingestion.failed").describe("Event type discriminator"), "payload": z.object({ 
/**URI of the artifact that failed ingestion*/
"artifact_uri": z.string().describe("URI of the artifact that failed ingestion"), 
/**Type of artifact*/
"artifact_kind": z.string().describe("Type of artifact"), 
/**Error message*/
"error_message": z.string().describe("Error message"), 
/**Error code if available*/
"error_code": z.union([z.string().describe("Error code if available"), z.null().describe("Error code if available")]).describe("Error code if available").optional(), 
/**Number of retry attempts*/
"retry_count": z.number().int().gte(0).describe("Number of retry attempts").optional(), 
/**Whether the error is retryable*/
"is_retryable": z.boolean().describe("Whether the error is retryable").optional() }) }).and(z.any()).describe("Artifact ingestion into RAG failed")
export type ArtifactIngestionFailedV1 = z.infer<typeof ArtifactIngestionFailedV1Schema>

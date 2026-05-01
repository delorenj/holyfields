import { z } from "zod"

/**Transcript was ingested into RAG system*/
export const FirefliesTranscriptProcessedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("fireflies.transcript.processed").describe("Event type discriminator"), "payload": z.object({ 
/**Fireflies transcript ID*/
"transcript_id": z.string().describe("Fireflies transcript ID"), 
/**Internal RAG document ID*/
"rag_document_id": z.string().describe("Internal RAG document ID"), 
/**Meeting title*/
"title": z.string().describe("Meeting title"), 
/**Number of sentences ingested*/
"sentence_count": z.number().int().gte(0).describe("Number of sentences ingested").optional(), 
/**Number of unique speakers*/
"speaker_count": z.number().int().gte(1).describe("Number of unique speakers").optional(), 
/**Duration in minutes*/
"duration_minutes": z.number().gte(0).describe("Duration in minutes").optional(), 
/**Vector store used (e.g., 'chroma', 'pinecone')*/
"vector_store": z.string().describe("Vector store used (e.g., 'chroma', 'pinecone')"), 
/**Number of chunks created*/
"chunk_count": z.number().int().gte(0).describe("Number of chunks created").optional(), 
/**Model used for embeddings*/
"embedding_model": z.union([z.string().describe("Model used for embeddings"), z.null().describe("Model used for embeddings")]).describe("Model used for embeddings").optional() }) }).and(z.any()).describe("Transcript was ingested into RAG system")
export type FirefliesTranscriptProcessedV1 = z.infer<typeof FirefliesTranscriptProcessedV1Schema>

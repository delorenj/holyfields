import { z } from "zod"

/**Event emitted when a new asset_registry row is inserted.*/
export const CreatedEventSchema = z.object({ "asset_id": z.string().uuid(), "agent_name": z.string().min(1), "asset_type": z.enum(["invite","font","coloring_page","mockup","listing_copy"]), "storage_uri": z.string().regex(new RegExp("^(file|gs|https|s3|volume)://")), "storage_provider": z.string().min(1), 
/**sha256 hash*/
"content_hash": z.string().describe("sha256 hash"), "prompt_text": z.union([z.string(), z.null()]).optional(), "model_provider": z.union([z.string(), z.null()]).optional(), "model_name": z.union([z.string(), z.null()]).optional(), "model_params_json": z.record(z.string(), z.any()).optional(), "source_event_id": z.union([z.string().uuid(), z.null()]).optional(), "correlation_id": z.string().uuid(), "lineage_parent_asset_id": z.union([z.string().uuid(), z.null()]).optional(), "status": z.enum(["active","revised","deleted"]), "created_at": z.string().datetime({ offset: true }), "updated_at": z.string().datetime({ offset: true }), "deleted_at": z.union([z.string().datetime({ offset: true }), z.null()]).optional() }).strict().describe("Event emitted when a new asset_registry row is inserted.")
export type CreatedEvent = z.infer<typeof CreatedEventSchema>

import { z } from "zod"

/**GitHub pull request was created*/
export const GithubPrCreatedV1Schema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("github.pr.created").describe("Event type discriminator"), "payload": z.object({ 
/**Key to retrieve PR data from cache (e.g., 'owner/repo/123')*/
"cache_key": z.string().describe("Key to retrieve PR data from cache (e.g., 'owner/repo/123')"), 
/**Type of cache storage*/
"cache_type": z.enum(["redis","memory","file"]).describe("Type of cache storage").optional(), 
/**Repository owner*/
"repo_owner": z.string().describe("Repository owner"), 
/**Repository name*/
"repo_name": z.string().describe("Repository name"), 
/**Pull request number*/
"pr_number": z.number().int().gte(1).describe("Pull request number") }) }).and(z.any()).describe("GitHub pull request was created")
export type GithubPrCreatedV1 = z.infer<typeof GithubPrCreatedV1Schema>

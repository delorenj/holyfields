import { z } from "zod"

/**Shared type definitions used across all 33GOD schemas*/
export const CommonTypesV1Schema = z.any().describe("Shared type definitions used across all 33GOD schemas")
export type CommonTypesV1 = z.infer<typeof CommonTypesV1Schema>

# Holyfields for TypeScript

`@33god/holyfields` provides Zod schemas and TypeScript types generated from
the Holyfields JSON Schema registry. The JSON Schemas remain the source of
truth; this package is a publishable TypeScript binding for services and
frontends that produce or consume 33GOD events.

## Use the package

Import generated schemas and types from the package root.

```ts
import { AgentSessionStartedV1Schema } from "@33god/holyfields";
```

The package also includes raw JSON Schemas under `schemas/` in published npm
tarballs.

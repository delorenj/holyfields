# Holyfields

Holyfields is the schema registry and contract package workspace for 33GOD.
JSON Schema is the source of truth. Python and TypeScript packages are generated
from those schemas and published as language-specific bindings.

## Repository model

Holyfields is one repository with package-per-language boundaries. Keep the
schemas centralized so contract changes generate, test, and drift-check across
all supported languages in one CI gate.

- `schemas/` contains versioned JSON Schemas.
- `packages/python/` publishes the `holyfields` Python package.
- `packages/typescript/` publishes the `@33god/holyfields` npm package.
- `tools/generators/` contains deterministic language generators.
- `scripts/` contains stable wrapper commands used by `mise` and CI.

Do not split Python and TypeScript into separate repositories unless release
ownership becomes fully independent. Today, atomic schema review is more
important than per-language repo autonomy.

## Commands

Use `mise` from the repository root.

| Task | Command |
| --- | --- |
| Install dependencies | `mise run install` |
| Validate schemas | `mise run validate:schemas` |
| Generate Python | `mise run generate:python` |
| Generate TypeScript | `mise run generate:typescript` |
| Generate all artifacts | `mise run generate:all` |
| Check generated drift | `mise run check:drift` |
| Test Python | `mise run test:python` |
| Test TypeScript | `mise run test:typescript` |
| Test all packages | `mise run test:all` |
| Typecheck packages | `mise run typecheck` |
| Build packages | `mise run build` |
| Full CI | `mise run ci` |

## Package usage

Use the generated language package that matches your service runtime.

Python services import Pydantic models from `holyfields.generated`.

```python
from holyfields.generated.agent.session_started_v1 import AgentSessionStartedV1
```

TypeScript services and frontends import Zod schemas from `@33god/holyfields`.

```ts
import { AgentSessionStartedV1Schema } from "@33god/holyfields";
```

Published packages include raw JSON Schemas for consumers that need runtime
schema validation or registry synchronization.

## Development workflow

Make contract changes through the schema source of truth.

1. Edit JSON Schema files in `schemas/`.
2. Run `mise run validate:schemas`.
3. Run `mise run generate:all`.
4. Run `mise run check:drift`.
5. Run `mise run ci` before opening a pull request.

Generated code is committed on purpose. Reviewers must be able to see the exact
consumer-facing Python and TypeScript changes caused by a schema edit.

## Adding another language

Add each new language as `packages/<language>`. The package must provide the
same contract as the existing packages:

- A deterministic generator that writes only inside that package.
- Committed generated artifacts.
- Package-specific tests and type checks.
- A build command that produces a publishable artifact.
- A root `mise` task wired into `generate:all`, `test:all`, `typecheck`,
  `check:drift`, and `ci`.

## Non-negotiables

- JSON Schema is the only source of truth.
- Never hand-edit generated package artifacts.
- Never keep generated drift in a pull request.
- Never exclude broken legacy tests from CI; delete, replace, or fix them.
- Keep `README.md`, `AGENTS.md`, `GOD.md`, and CI aligned with the package
  layout.

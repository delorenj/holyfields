# Holyfields - Agent Guide

Holyfields is the 33GOD event schema registry and contract package workspace.
JSON Schema is the source of truth. Language packages are generated from those
schemas.

## Architecture

- `schemas/` contains versioned JSON Schemas.
- `packages/python/` publishes the `holyfields` Python package with generated
  Pydantic models.
- `packages/typescript/` publishes the `@33god/holyfields` npm package with
  generated Zod schemas and TypeScript types.
- `tools/generators/` contains deterministic generators.
- `scripts/` contains stable command wrappers for `mise` and CI.

## Commands

| Task | Command |
| --- | --- |
| Install deps | `mise run install` |
| Generate Python | `mise run generate:python` |
| Generate TypeScript | `mise run generate:typescript` |
| Generate all | `mise run generate:all` |
| Validate schemas | `mise run validate:schemas` |
| Test Python | `mise run test:python` |
| Test TypeScript | `mise run test:typescript` |
| Test all | `mise run test:all` |
| Typecheck | `mise run typecheck` |
| Check drift | `mise run check:drift` |
| Build packages | `mise run build` |
| Full CI | `mise run ci` |

## Workflow

1. Edit JSON Schema files in `schemas/`.
2. Run `mise run validate:schemas`.
3. Run `mise run generate:all`.
4. Run `mise run check:drift`.
5. Run `mise run ci` before committing.

## Anti-patterns

- Never hand-edit generated code in `packages/*/src/generated` or
  `packages/python/src/holyfields/generated`.
- Never add fields directly to generated Pydantic or Zod artifacts.
- Never leave language artifacts out of sync with `schemas/`.
- Never keep excluded legacy tests as silent debt.
- Never split language packages into separate repos unless schema ownership and
  release ownership become independent.

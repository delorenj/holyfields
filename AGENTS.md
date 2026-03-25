# Holyfields — Agent Guide

Event schema registry and contract system. JSON Schema is the single source of truth; Python (Pydantic) and TypeScript (Zod) artifacts are generated.

## Tech Stack

- **Source of Truth:** JSON Schema
- **Python:** Pydantic models (generated via datamodel-code-generator)
- **TypeScript:** Zod schemas (generated)
- **Tools:** Python 3.12, Node 20, uv, bun

## Commands (mise)

| Task | Command |
|------|---------|
| Install deps | `mise run install` |
| Generate Python | `mise run generate:python` |
| Generate TypeScript | `mise run generate:typescript` |
| Generate All | `mise run generate:all` |
| Validate Schemas | `mise run validate:schemas` |
| Test Python | `mise run test:python` (pytest) |
| Test TypeScript | `mise run test:typescript` (bun test) |
| Test All | `mise run test:all` |
| Type Check | `mise run typecheck` (mypy + tsc) |
| Check Drift | `mise run check:drift` |
| Full CI | `mise run ci` |

## Workflow

1. Edit JSON Schema files in `schemas/`
2. Run `mise run generate:all` to regenerate language bindings
3. Run `mise run check:drift` to verify no uncommitted drift
4. Run `mise run ci` before committing

## Anti-Patterns

- **Never** hand-edit generated code in `generated/` — always modify the JSON Schema source
- **Never** add fields to Pydantic/Zod models directly — schema drift will break CI
- **Never** skip `check:drift` before committing schema changes

# Enterprise cleanup migration note

This note documents the April 30, 2026, Holyfields repository cleanup. The
change is intentionally breaking because Holyfields has no production package
consumers yet.

## What changed

Holyfields moved from a flat mixed Python and TypeScript repository to a
package-per-language workspace.

- Python now lives in `packages/python` and publishes as `holyfields`.
- TypeScript now lives in `packages/typescript` and publishes as
  `@33god/holyfields`.
- Generators now live in `tools/generators`.
- Generated artifacts are committed inside their owning language packages.
- Legacy generated trees and excluded legacy tests were removed.

## How to work after the cleanup

Use root `mise` tasks for normal development.

1. Edit schemas in `schemas/`.
2. Run `mise run generate:all`.
3. Run `mise run check:drift`.
4. Run `mise run ci`.

Import generated Python models from `holyfields.generated`. Import generated
TypeScript schemas from `@33god/holyfields`.

## Why the repo stayed together

Holyfields is a contract registry, not two independent applications. Keeping
language packages in one repository lets the team review one schema change and
the resulting Python and TypeScript impact together.

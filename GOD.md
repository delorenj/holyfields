# Holyfields GOD

Holyfields defines the 33GOD event and command contracts. If a contract is not
defined in `schemas/`, it is not part of the platform contract surface.

## Current architecture

Holyfields is a single schema registry with publishable language packages.

- Source of truth: `schemas/**/*.v1.json`.
- Python package: `packages/python`, published as `holyfields`.
- TypeScript package: `packages/typescript`, published as `@33god/holyfields`.
- Generators: `tools/generators`.
- CI gate: schema validation, generation, drift checks, type checks, tests, and
  package builds.

This repository intentionally keeps all language packages together. Contract
changes must be reviewed atomically across every generated binding.

## Contract rules

- Events are immutable facts.
- Commands are mutable requests.
- JSON Schema owns wire shape, required fields, enum values, and versioning.
- Generated language artifacts are committed for reviewability.
- Consumers import language packages; producers do not invent local event
  models.

## Package boundaries

The root repository orchestrates work. It is not a publishable runtime package.

`packages/python` owns Python runtime metadata, tests, and generated Pydantic
models. Generated imports use `holyfields.generated`.

`packages/typescript` owns npm metadata, tests, and generated Zod schemas.
Generated imports use `@33god/holyfields`.

Future languages must follow the same package contract: deterministic
generation, committed artifacts, tests, type checks, and build validation.

## Operating workflow

Use `mise` from the repository root.

1. Change schemas in `schemas/`.
2. Run `mise run validate:schemas`.
3. Run `mise run generate:all`.
4. Run `mise run check:drift`.
5. Run `mise run ci`.

No pull request is healthy if generated drift exists or if a language package
cannot build.

## Enterprise posture

Holyfields is treated as infrastructure. The repository must make ownership,
release surfaces, and failure modes obvious:

- One authoritative README.
- One agent guide.
- One CI gate.
- No hidden skipped tests.
- No stale generated trees.
- No production compatibility promises before production consumers exist.

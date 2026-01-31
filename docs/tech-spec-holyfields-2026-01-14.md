# Technical Specification: Holyfields

**Date:** 2026-01-14
**Author:** Jarad DeLorenzo
**Version:** 1.0
**Project Type:** library
**Project Level:** 1
**Status:** Draft

---

## Document Overview

This Technical Specification provides focused technical planning for Holyfields. It is designed for smaller projects (Level 0-1) that need clear requirements without heavyweight PRD overhead.

**Related Documents:**

- Product Brief: docs/product-brief-holyfields-2026-01-14.md

---

## Problem & Solution

### Problem Statement

When developing TheBoard (Python backend) and TheBoardroom (TypeScript frontend) in parallel with separate Claude agents, event schema mismatches occur frequently. TheBoard added events with specific schemas, but TheBoardroom mocked events with foreign naming conventions, wrong hierarchy, missing events, and invented events not in the plan. This led to silent data loss, missing UI updates, and fake updates where mocking behavior masquerades as real behavior.

### Proposed Solution

Holyfields as a centralized event schema registry using JSON Schema as source of truth, with automated generation of language-specific artifacts (Python Pydantic, TypeScript Zod/types, future Rust serde structs). Contract validation integrated into component CI pipelines catches violations before runtime. Per-component semantic versioning enables parallel development without coordination bottlenecks.

---

## Requirements

### What Needs to Be Built

1. **JSON Schema Infrastructure** - Schema storage and validation framework with per-component versioning
   - Acceptance: All schemas validate against JSON Schema Draft 2020-12, semantic versioning enforced

2. **Python Code Generation** - Pydantic models auto-generated from JSON Schema
   - Acceptance: Generated models pass mypy strict type checking, all fields have correct types

3. **TypeScript Code Generation** - Zod schemas + types auto-generated from JSON Schema
   - Acceptance: Generated code passes tsc strict mode, Zod validation works at runtime

4. **TheBoard Contract Definitions** - Complete command + event schemas for TheBoard component
   - Acceptance: All 7 TheBoard events defined (meeting.created, meeting.started, round.completed, comment.extracted, converged, completed, failed)

5. **TheboardRoom Contract Definitions** - Event schemas for TheboardRoom consumer
   - Acceptance: All consumed TheBoard events have consumer-side schemas with UI-specific metadata

6. **Contract Test Framework** - Schema conformance validation tests
   - Acceptance: pytest suite validates all Python artifacts, vitest suite validates all TypeScript artifacts, 100% schema coverage

7. **CI Pipeline Integration** - Pre-commit hooks + GitHub Actions for validation
   - Acceptance: PR validation blocks merge on schema errors, breaking changes detected automatically

8. **Event Catalog Documentation** - Human-readable docs with usage examples
   - Acceptance: Each event has markdown doc with description, fields, producer/consumer examples, versioning notes

### What This Does NOT Include

- Runtime validation libraries in consuming services (components implement their own validation)
- Event routing logic or Bloodbank client wrappers (responsibility of Bloodbank infrastructure)
- Monitoring/tracing instrumentation (responsibility of individual components)
- Migration tooling for schema evolution (future phase)
- CLI tools for schema generation/validation (CI-driven only for v1)
- Auto-discovery or registry service (static contracts in git for v1)

---

## Technical Approach

### Technology Stack

- **Schema Definition:** JSON Schema Draft 2020-12 (source of truth)
- **Python Generation:** `datamodel-code-generator` (JSON Schema → Pydantic)
- **TypeScript Generation:** `json-schema-to-zod` (JSON Schema → Zod schemas + TS types)
- **Python Validation:** `jsonschema` library + pytest
- **TypeScript Validation:** `ajv` (JSON Schema validator) + vitest
- **CI/CD:** GitHub Actions + pre-commit hooks
- **Version Control:** Git with semantic versioning per component directory
- **Package Management:** uv (Python), bun (TypeScript)
- **Task Runner:** mise tasks for generation scripts

### Architecture Overview

```
Holyfields/
├── common/                    # Shared base types, enums
│   └── schemas/              # JSON Schema definitions
│       ├── base_envelope.json
│       ├── timestamp.json
│       └── status_enum.json
├── theboard/                  # TheBoard component contracts
│   ├── commands/             # Command schemas (mutable events)
│   ├── events/               # Event schemas (immutable results)
│   │   ├── meeting_created.json
│   │   ├── meeting_started.json
│   │   ├── round_completed.json
│   │   ├── comment_extracted.json
│   │   ├── converged.json
│   │   ├── completed.json
│   │   └── failed.json
│   └── schemas/              # Root schema files with $ref to events
├── theboardroom/             # TheboardRoom component contracts
│   └── events/               # Event schemas (consumer-side)
│       └── (mirrors theboard events with UI metadata)
├── generated/                # Auto-generated language artifacts (gitignored or committed TBD)
│   ├── python/               # Pydantic models
│   │   ├── common/
│   │   ├── theboard/
│   │   └── theboardroom/
│   └── typescript/           # Zod schemas + TS types
│       ├── common/
│       ├── theboard/
│       └── theboardroom/
├── tests/                    # Contract validation tests
│   ├── python/               # pytest suites
│   └── typescript/           # vitest suites
├── docs/                     # Event catalog + usage examples
│   ├── catalog/              # Per-event documentation
│   └── guides/               # Integration guides
├── scripts/                  # Generation + CI scripts
│   ├── generate_python.sh
│   ├── generate_typescript.sh
│   └── validate_schemas.sh
├── .github/
│   └── workflows/
│       └── validate-contracts.yml
├── .pre-commit-config.yaml
├── mise.toml                 # Task definitions
├── pyproject.toml            # Python dependencies
├── package.json              # TypeScript dependencies
└── README.md
```

**Data Flow:**

1. Developer defines event in JSON Schema (e.g., `theboard/events/meeting_created.json`)
2. Pre-commit hook validates schema structure before commit
3. On push, GitHub Actions triggers validation + code generation
4. Generation scripts create Pydantic models in `generated/python/`
5. Generation scripts create Zod schemas + TS types in `generated/typescript/`
6. Contract tests validate generated artifacts match schema expectations
7. Consuming services import generated artifacts as dependencies

**Versioning Strategy:**

- Each component directory (theboard/, theboardroom/) has independent semantic versioning
- Schema changes increment version in component metadata file
- Breaking changes (field removal, type change) increment major version
- Additive changes (new optional field) increment minor version
- Documentation/comment changes increment patch version

### Data Model (if applicable)

**Base Event Envelope (common/schemas/base_envelope.json):**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "event_type": {
      "type": "string",
      "description": "Event identifier (e.g., theboard.meeting.created)"
    },
    "event_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique event ID"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Schema version (semver)"
    },
    "producer": {
      "type": "string",
      "description": "Service that emitted event"
    },
    "payload": { "type": "object", "description": "Event-specific data" }
  },
  "required": [
    "event_type",
    "event_id",
    "timestamp",
    "version",
    "producer",
    "payload"
  ]
}
```

**Example TheBoard Event (theboard/events/meeting_created.json):**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://holyfields/theboard/events/meeting_created.json",
  "title": "MeetingCreated",
  "description": "Emitted when a new meeting is initialized",
  "allOf": [{ "$ref": "../../common/schemas/base_envelope.json" }],
  "properties": {
    "payload": {
      "type": "object",
      "properties": {
        "meeting_id": { "type": "string", "format": "uuid" },
        "topic": { "type": "string" },
        "max_rounds": { "type": "integer", "minimum": 1 },
        "model": { "type": "string" },
        "agents": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string", "format": "uuid" },
              "name": { "type": "string" },
              "expertise": { "type": "string" }
            },
            "required": ["id", "name", "expertise"]
          }
        }
      },
      "required": ["meeting_id", "topic", "max_rounds", "model", "agents"]
    }
  }
}
```

### API Design (if applicable)

Not applicable. This is a library/contract repository, not an API service. Contracts are consumed via generated code artifacts, not runtime API calls.

---

## Implementation Plan

### Stories

1. **Repository Infrastructure** - Initialize repo with directory structure, README, gitignore, mise tasks for tooling
   - Deliverable: Complete repo skeleton with package.json, pyproject.toml, mise.toml, directory structure

2. **Common Base Schemas** - Define shared types (timestamps, IDs, status enums, base event envelope)
   - Deliverable: common/schemas/ with base_envelope.json, timestamp.json, status_enum.json, all validated

3. **TheBoard Event Schemas** - Define all TheBoard events from current implementation
   - Deliverable: 7 event schemas in theboard/events/, all referencing common base

4. **Python Generation Pipeline** - Script using datamodel-code-generator to create Pydantic models from JSON Schema
   - Deliverable: scripts/generate_python.sh, generated/python/ with valid Pydantic models, mise task `mise run generate:python`

5. **TypeScript Generation Pipeline** - Script using json-schema-to-zod to create Zod schemas + TS types
   - Deliverable: scripts/generate_typescript.sh, generated/typescript/ with valid Zod schemas, mise task `mise run generate:typescript`

6. **Contract Test Framework** - pytest + vitest suites that validate generated artifacts against schemas
   - Deliverable: tests/python/ with pytest suite (100% schema coverage), tests/typescript/ with vitest suite (100% coverage)

7. **CI Integration** - GitHub Actions workflow + pre-commit hooks for validation and generation
   - Deliverable: .github/workflows/validate-contracts.yml, .pre-commit-config.yaml, breaking change detection

8. **Event Catalog Documentation** - Markdown docs with usage examples for each event type
   - Deliverable: docs/catalog/ with one .md per event, docs/guides/ with integration examples

### Development Phases

**Phase 1: Foundation (Stories 1-2)**

- Goal: Repository infrastructure + common base schemas
- Outcome: Ready for component-specific schema definition

**Phase 2: TheBoard Contracts (Story 3)**

- Goal: Define all TheBoard event schemas
- Outcome: Complete JSON Schema definitions for TheBoard component

**Phase 3: Code Generation (Stories 4-5)**

- Goal: Automated Python + TypeScript artifact generation
- Outcome: Validated Pydantic models and Zod schemas from all TheBoard schemas

**Phase 4: Validation & CI (Stories 6-7)**

- Goal: Contract tests + automated CI validation
- Outcome: 100% test coverage, PR validation prevents bad schemas from merging

**Phase 5: Documentation (Story 8)**

- Goal: Human-readable event catalog
- Outcome: Developers can browse event docs and understand how to use contracts

---

## Acceptance Criteria

How we'll know it's done:

- [ ] Repository initialized with complete directory structure (common/, theboard/, theboardroom/, generated/, tests/, docs/, scripts/)
- [ ] Common base schemas defined (event envelope, timestamps, IDs, status enums) and validated against JSON Schema Draft 2020-12
- [ ] All TheBoard events from current implementation defined as JSON Schemas (meeting.created, meeting.started, round.completed, comment.extracted, converged, completed, failed)
- [ ] Python generation script produces valid Pydantic models from all schemas (passes mypy strict)
- [ ] TypeScript generation script produces valid Zod schemas and TS types from all schemas (passes tsc strict)
- [ ] Contract tests pass for all generated Python artifacts (pytest suite validates schema conformance, 100% coverage)
- [ ] Contract tests pass for all generated TypeScript artifacts (vitest suite validates schema conformance, 100% coverage)
- [ ] GitHub Actions workflow runs on PR and validates all schemas + generated artifacts
- [ ] Pre-commit hooks lint schemas and block commits with validation errors
- [ ] Event catalog documentation complete with usage examples for each TheBoard event
- [ ] TheBoard component can import and use generated Python contracts (integration validated)
- [ ] TheBoardroom component can import and use generated TypeScript contracts (integration validated)
- [ ] Breaking change detection catches schema incompatibilities in CI (tested with intentional breaking change)
- [ ] 100% of in-scope TheBoard events have contracts defined (7/7 events)

---

## Non-Functional Requirements

### Performance

- Schema validation must complete in CI within 2 minutes (entire workflow)
- Code generation must complete in < 30 seconds per component
- Generated Python models must have zero runtime overhead vs hand-written Pydantic
- Generated TypeScript types must not increase bundle size (tree-shakeable)

### Security

- No secrets or credentials in schemas (all schemas are public contracts)
- All generated Python code must pass `bandit` security linting
- All generated TypeScript code must pass `eslint` with security rules enabled
- GitHub Actions must use minimal permissions (read-only except for status checks)

### Other

- **Maintainability:** All schemas must include `description` fields for self-documentation. Generated code must include comments with link back to source schema file.
- **Compatibility:** Support Python 3.11+ (TheBoard requirement), TypeScript 5.0+ (TheBoardroom requirement)
- **Portability:** Generation scripts must work on Linux, macOS (development environments)
- **Observability:** CI logs must show which schemas were validated, which artifacts were generated, and any breaking changes detected

---

## Dependencies

- **TheBoard** must have stable event emission implementation (already exists at ../../theboard/trunk-main)
- **RabbitMQ/Bloodbank** infrastructure must be available for integration validation (already exists at ../../bloodbank/trunk-main)
- **GitHub Actions** must have necessary permissions for automated commits if generated artifacts are committed (TBD: decide if artifacts are gitignored or committed)
- **Package registries:** PyPI availability for datamodel-code-generator, npm registry for json-schema-to-zod

---

## Risks & Mitigation

- **Risk:** Code generation tooling gaps (Medium likelihood)
  - **Impact:** Generated artifacts may not match JSON Schema semantics perfectly
  - **Mitigation:** Start with Python only (datamodel-code-generator is mature), validate approach thoroughly, then add TypeScript. Run extensive test suite against generated code.

- **Risk:** Schema versioning complexity (Medium likelihood)
  - **Impact:** Managing multiple concurrent schema versions may introduce confusion
  - **Mitigation:** Start with single version (1.0.0) for all schemas. Defer multi-version support to future phase. Document breaking vs non-breaking changes clearly.

- **Risk:** Generated code size (Low likelihood)
  - **Impact:** Generated artifacts may bloat repository size if committed
  - **Mitigation:** Monitor generated artifact size. If > 1MB per language, add to gitignore and generate during CI or component build. Use git-lfs if artifacts must be committed.

- **Risk:** Adoption resistance from components (Low likelihood)
  - **Impact:** TheBoard or TheBoardroom may not integrate contract validation
  - **Mitigation:** Make integration trivial (single import line). Create clear integration guide. Demonstrate value with TheBoard/TheBoardroom as reference implementation.

---

## Timeline

**Target Completion:** M effort (schema infrastructure + initial contracts + CI validation)

**Milestones:**

1. Repository infrastructure complete (S effort)
2. Common base schemas + Python generation working (M effort)
3. TheBoard events defined + TypeScript generation working (M effort)
4. Contract tests passing (S effort)
5. CI integration complete (S effort)
6. Documentation ready (S effort)

**Critical Path:** Stories 1 → 2 → 3 → 4/5 (parallel) → 6 → 7 → 8

---

## Approval

**Reviewed By:**

- [ ] Jarad DeLorenzo (Author)
- [ ] Technical Lead (N/A - solo project)
- [ ] Product Owner (N/A - internal tool)

---

## Next Steps

### Phase 4: Implementation

For Level 1 projects (1-10 stories):

- Run `/sprint-planning` to plan your sprint
- Then create and implement stories

---

**This document was created using BMAD Method v6 - Phase 2 (Planning)**

_To continue: Run `/workflow-status` to see your progress and next recommended workflow._

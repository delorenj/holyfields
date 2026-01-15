# Sprint Plan: bloodbank-contracts

**Date:** 2026-01-14
**Scrum Master:** Jarad DeLorenzo
**Project Level:** 1
**Total Stories:** 8
**Total Points:** 33
**Planned Sprints:** 1

---

## Executive Summary

This sprint plan establishes the bloodbank-contracts event schema registry for the 33GOD ecosystem. The single sprint delivers complete JSON Schema infrastructure, Python and TypeScript code generation pipelines, TheBoard event contracts, contract validation tests, CI integration, and documentation. This enables TheBoard and TheBoardroom to develop independently with guaranteed schema compatibility.

**Key Metrics:**
- Total Stories: 8
- Total Points: 33
- Sprints: 1 (2 weeks)
- Team Capacity: 30 points per sprint (1 senior developer)
- Target Completion: 2026-01-28 (2 weeks from start)

---

## Story Inventory

### STORY-001: Repository Infrastructure

**Priority:** Must Have (Foundation)
**Estimate:** 2 points (S effort)

**User Story:**
As a developer
I want a properly initialized repository with tooling and directory structure
So that I can begin defining schemas and generating code

**Acceptance Criteria:**
- [ ] Repository initialized at /home/delorenj/code/33GOD/bloodbank-contracts/
- [ ] Directory structure created (common/, theboard/, theboardroom/, generated/, tests/, docs/, scripts/)
- [ ] package.json with TypeScript dependencies (json-schema-to-zod, ajv, vitest, etc.)
- [ ] pyproject.toml with Python dependencies (datamodel-code-generator, jsonschema, pytest, etc.)
- [ ] mise.toml with task definitions (generate:python, generate:typescript, test:all, validate:schemas)
- [ ] README.md with project overview and quick start
- [ ] .gitignore configured (generated/ artifacts decision TBD)

**Technical Notes:**
- Use uv for Python package management
- Use bun for TypeScript package management
- mise tasks will be primary developer interface

**Dependencies:** None (foundation story)

---

### STORY-002: Common Base Schemas

**Priority:** Must Have (Foundation)
**Estimate:** 3 points (S-M effort)

**User Story:**
As a schema author
I want shared base types and enums defined
So that all component schemas can reference common structures consistently

**Acceptance Criteria:**
- [ ] common/schemas/base_envelope.json defined with event_type, event_id, timestamp, version, producer, payload
- [ ] common/schemas/timestamp.json with ISO 8601 format validation
- [ ] common/schemas/status_enum.json with standard status values
- [ ] All schemas validate against JSON Schema Draft 2020-12
- [ ] $id and $schema fields present in all schemas
- [ ] Description fields present for all properties

**Technical Notes:**
- Base envelope uses allOf pattern for composition
- All component events will extend base_envelope
- Semantic versioning enforced in version field (pattern: "^\d+\.\d+\.\d+$")

**Dependencies:** STORY-001 (requires directory structure)

---

### STORY-003: TheBoard Event Schemas

**Priority:** Must Have (Core Value)
**Estimate:** 5 points (M effort)

**User Story:**
As a TheBoard developer
I want all TheBoard events defined as JSON Schemas
So that consumers have guaranteed event structure contracts

**Acceptance Criteria:**
- [ ] 7 event schemas defined in theboard/events/:
  - meeting_created.json
  - meeting_started.json
  - round_completed.json
  - comment_extracted.json
  - converged.json
  - completed.json
  - failed.json
- [ ] All schemas extend common/schemas/base_envelope.json
- [ ] All payload fields have types, descriptions, and required constraints
- [ ] Schemas match current TheBoard event emission implementation
- [ ] $ref links validated and working

**Technical Notes:**
- Reference existing TheBoard implementation at ../../theboard/trunk-main/src/theboard/events/
- Payload structures must match EventEmitter usage
- Version all schemas as 1.0.0 initially

**Dependencies:** STORY-002 (requires base schemas)

---

### STORY-004: Python Generation Pipeline

**Priority:** Must Have (Core Value)
**Estimate:** 5 points (M-L effort)

**User Story:**
As a Python developer
I want Pydantic models auto-generated from JSON Schemas
So that I can import type-safe contracts in Python services

**Acceptance Criteria:**
- [ ] scripts/generate_python.sh created and executable
- [ ] Generation uses datamodel-code-generator with correct flags
- [ ] Generated Pydantic models in generated/python/ directory structure mirrors schemas
- [ ] All generated models pass mypy strict type checking
- [ ] mise task `mise run generate:python` executes successfully
- [ ] Generated code includes comments linking to source schema

**Technical Notes:**
- Use datamodel-code-generator v0.25+ for JSON Schema Draft 2020-12 support
- Generate to generated/python/common/, generated/python/theboard/, etc.
- Include BaseModel imports and proper typing

**Dependencies:** STORY-002, STORY-003 (requires schemas to generate from)

---

### STORY-005: TypeScript Generation Pipeline

**Priority:** Must Have (Core Value)
**Estimate:** 5 points (M-L effort)

**User Story:**
As a TypeScript developer
I want Zod schemas and TypeScript types auto-generated from JSON Schemas
So that I can import type-safe contracts in TypeScript services

**Acceptance Criteria:**
- [ ] scripts/generate_typescript.sh created and executable
- [ ] Generation uses json-schema-to-zod with correct configuration
- [ ] Generated code in generated/typescript/ with directory structure mirroring schemas
- [ ] All generated code passes tsc strict mode
- [ ] Zod validation works at runtime
- [ ] mise task `mise run generate:typescript` executes successfully
- [ ] Generated code includes comments linking to source schema

**Technical Notes:**
- Use json-schema-to-zod or similar tool (evaluate alternatives if needed)
- Generate both Zod schemas and TypeScript interfaces
- Ensure tree-shakeable exports

**Dependencies:** STORY-002, STORY-003 (requires schemas to generate from)

---

### STORY-006: Contract Test Framework

**Priority:** Must Have (Validation)
**Estimate:** 5 points (M effort)

**User Story:**
As a developer
I want automated tests that validate generated artifacts
So that I can trust contracts are correctly implemented

**Acceptance Criteria:**
- [ ] tests/python/ with pytest suite validating all Python artifacts
- [ ] tests/typescript/ with vitest suite validating all TypeScript artifacts
- [ ] 100% schema coverage (every schema has tests)
- [ ] Tests validate:
  - Generated code matches schema structure
  - Required fields are enforced
  - Type validation works correctly
  - $ref resolution works
- [ ] mise task `mise run test:all` runs both test suites
- [ ] All tests passing

**Technical Notes:**
- Python tests use pytest with jsonschema library for validation
- TypeScript tests use vitest with ajv for JSON Schema validation
- Test both generated artifacts and raw schemas

**Dependencies:** STORY-004, STORY-005 (requires generated artifacts to test)

---

### STORY-007: CI Integration

**Priority:** Must Have (Automation)
**Estimate:** 5 points (M effort)

**User Story:**
As a developer
I want automated CI validation on every PR
So that invalid schemas cannot be merged

**Acceptance Criteria:**
- [ ] .github/workflows/validate-contracts.yml created
- [ ] GitHub Actions workflow validates:
  - All schemas against JSON Schema Draft 2020-12
  - Python code generation succeeds
  - TypeScript code generation succeeds
  - All contract tests pass
  - Breaking changes detected (compares to main)
- [ ] .pre-commit-config.yaml configured with schema linting
- [ ] Pre-commit hooks block commits with schema validation errors
- [ ] Workflow runs on pull_request and push to main
- [ ] Workflow completes in < 2 minutes

**Technical Notes:**
- Use check-jsonschema for pre-commit schema validation
- GitHub Actions uses mise tasks for generation and testing
- Breaking change detection: compare schema field removals and type changes

**Dependencies:** STORY-006 (requires test framework), STORY-004, STORY-005 (requires generation scripts)

---

### STORY-008: Event Catalog Documentation

**Priority:** Should Have (Developer Experience)
**Estimate:** 3 points (S-M effort)

**User Story:**
As a developer
I want human-readable documentation for each event
So that I can understand event structures without reading JSON Schema

**Acceptance Criteria:**
- [ ] docs/catalog/ directory created
- [ ] One markdown file per TheBoard event (7 files total)
- [ ] Each doc includes:
  - Event description
  - Field table (name, type, required, description)
  - Example payload (JSON)
  - Producer example (Python code showing how to emit)
  - Consumer example (TypeScript code showing how to consume)
  - Version history
- [ ] docs/guides/integration.md with integration instructions for components
- [ ] README.md updated with link to catalog

**Technical Notes:**
- Auto-generate initial docs from schemas if possible (script in scripts/)
- Manual refinement of descriptions and examples
- Keep docs in sync with schemas (document in CONTRIBUTING.md)

**Dependencies:** STORY-003 (requires event schemas)

---

## Sprint Allocation

### Sprint 1 (Weeks 1-2) - 33/30 points

**Goal:** Establish complete contract infrastructure with TheBoard events, automated generation, CI validation, and documentation

**Stories:**
- STORY-001: Repository Infrastructure (2 points) - Must Have
- STORY-002: Common Base Schemas (3 points) - Must Have
- STORY-003: TheBoard Event Schemas (5 points) - Must Have
- STORY-004: Python Generation Pipeline (5 points) - Must Have
- STORY-005: TypeScript Generation Pipeline (5 points) - Must Have
- STORY-006: Contract Test Framework (5 points) - Must Have
- STORY-007: CI Integration (5 points) - Must Have
- STORY-008: Event Catalog Documentation (3 points) - Should Have

**Total:** 33 points / 30 capacity (110% utilization - acceptable with buffer strategy)

**Mitigation Strategy:**
- STORY-008 is "Should Have" - can be deferred if time pressure emerges
- Stories 004 and 005 can be parallelized (work on TypeScript while Python generation builds)
- If running over, complete STORY-008 in post-sprint cleanup

**Risks:**
- **Medium:** Code generation tooling may have unexpected gaps - Mitigation: Start with Python (more mature), prototype early
- **Low:** Schema complexity for TheBoard events unknown - Mitigation: Reference existing TheBoard implementation closely

**Dependencies:**
- None external - all work is self-contained within bloodbank-contracts repo
- TheBoard implementation exists for reference at ../../theboard/trunk-main

---

## Requirements Coverage

All 8 requirements from tech spec are covered:

| Requirement ID | Requirement | Story | Sprint |
|----------------|-------------|-------|--------|
| REQ-001 | JSON Schema Infrastructure | STORY-001, STORY-002 | 1 |
| REQ-002 | Python Code Generation | STORY-004 | 1 |
| REQ-003 | TypeScript Code Generation | STORY-005 | 1 |
| REQ-004 | TheBoard Contract Definitions | STORY-003 | 1 |
| REQ-005 | TheboardRoom Contract Definitions | Deferred to Phase 2 | - |
| REQ-006 | Contract Test Framework | STORY-006 | 1 |
| REQ-007 | CI Pipeline Integration | STORY-007 | 1 |
| REQ-008 | Event Catalog Documentation | STORY-008 | 1 |

**Note:** REQ-005 (TheboardRoom contracts) deferred to validate approach with TheBoard first. Can be added in follow-up sprint if needed.

---

## Risks and Mitigation

**High:**
- None identified

**Medium:**
- **Code generation tooling gaps** - datamodel-code-generator or json-schema-to-zod may not handle all JSON Schema features
  - **Mitigation:** Prototype both tools early in STORY-004/005. If gaps found, consider alternative tools (pydantic-gen, quicktype) or manual template generation

- **Schema design complexity** - TheBoard events may have complex nested structures
  - **Mitigation:** Reference existing TheBoard EventEmitter implementation closely. Start with simplest event (meeting.created) to validate approach

**Low:**
- **Performance of generation scripts** - may take too long in CI
  - **Mitigation:** Target < 30 seconds per language. Optimize scripts or use caching if needed

- **Breaking change detection complexity** - git diff of JSON Schema may be brittle
  - **Mitigation:** Simple field/type comparison sufficient for v1. Defer sophisticated schema diffing to future

---

## Dependencies

**Internal:**
- None - all stories are within bloodbank-contracts scope

**External:**
- **TheBoard repository** (../../theboard/trunk-main) - reference for existing event structures (read-only dependency)
- **GitHub Actions** - requires repository access and workflow permissions
- **Package registries** - PyPI for Python packages, npm registry for TypeScript packages

---

## Definition of Done

For a story to be considered complete:
- [ ] Code implemented and committed to main branch
- [ ] All acceptance criteria met and validated
- [ ] Unit tests written and passing (≥80% coverage where applicable)
- [ ] Integration tests passing (contract tests for generation stories)
- [ ] Code reviewed (self-review for solo project, but must validate against standards)
- [ ] Documentation updated (README, catalog docs, inline comments)
- [ ] CI validation passing (schema validation, generation, tests)
- [ ] Demo-able (can show working artifact generation or validation)

---

## Next Steps

**Immediate:** Begin Sprint 1

**Option 1: Create detailed story documents**
Run `/create-story STORY-001` to generate individual story files in docs/stories/

**Option 2: Start implementing immediately** (recommended for Level 1)
Run `/dev-story STORY-001` to begin implementation of Repository Infrastructure

**Sprint Cadence:**
- Sprint length: 2 weeks
- Sprint start: 2026-01-14
- Sprint end: 2026-01-28
- Sprint review: 2026-01-28
- Sprint retrospective: 2026-01-28

**Implementation Order:**
1. STORY-001 (Foundation)
2. STORY-002 (Base schemas)
3. STORY-003 (TheBoard events)
4. STORY-004 + STORY-005 (Generation pipelines - can parallelize)
5. STORY-006 (Contract tests)
6. STORY-007 (CI integration)
7. STORY-008 (Documentation)

---

**This plan was created using BMAD Method v6 - Phase 4 (Implementation Planning)**

*To continue: Run `/dev-story STORY-001` to begin implementation or `/workflow-status` to check progress.*

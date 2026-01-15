# Product Brief: bloodbank-contracts

**Date:** 2026-01-14
**Author:** Jarad DeLorenzo
**Version:** 1.0
**Project Type:** library
**Project Level:** 1

---

## Executive Summary

I'm building a microservice-to-microservice contract system to facilitate async communication/coordination between two or more parallel LLM coding agents. This repo will act as a version controlled source of truth for each 33GOD component's Bloodbank event schema. Since the primary agentic entrypoint to each service will be a Bloodbank command (mutable event), and all services broadcast their responses/results via Bloodbank event (immutable event), this repo will allow each service to be developed independently with guarantees that any dependencies will integrate seamlessly, provided they adhere to this repo's defined service contracts.

---

## Problem Statement

### The Problem

When developing TheBoard (Python backend) and TheBoardroom (TypeScript frontend) in parallel with separate Claude agents, event schema mismatches occur frequently. TheBoard added events with specific schemas, but TheBoardroom mocked events with foreign naming conventions, wrong hierarchy, missing events, and invented events not in the plan. This led to silent data loss, missing UI updates, and fake updates where mocking behavior masquerades as real behavior.

### Why Now?

The 33GOD ecosystem is growing beyond 2-3 components to 7+ services (TheBoard, TheBoardroom, Flume, Holocene, iMi, Jelmore, 00_ceiling, Yi, Zellij-driver, Candybar). Without a contract-first approach, the coordination overhead and risk of runtime failures grows exponentially. The coupling is currently so loose that developers know results will be incorrect during development. PRD entropy over weeks/months exacerbates this as requirements become outdated faster than implementation can catch up.

### Impact if Unsolved

Development velocity will continue to degrade as manual cross-repo coordination becomes bottleneck. Runtime event parsing failures will increase. Silent data loss and UI bugs will erode system reliability. Integration testing across 5+ services will become prohibitively complex. The 'Director of Engineering' meta-BMAD approach (conversation history at /home/delorenj/code/33GOD) will remain a mental model rather than formal automation, increasing cognitive load on Jarad as sole orchestrator.

---

## Target Audience

### Primary Users

LLM coding agents (Claude instances) working on individual 33GOD components, and Jarad DeLorenzo as orchestrator. These agents need to trust that schemas are current and accurate, validate contracts quickly (< S effort), and receive clear notifications when breaking changes occur.

### Secondary Users

Future Letta 'Director of Engineering' agent for cross-repo workflow orchestration, CI/CD systems (GitHub Actions) for automated contract enforcement, and Candybar (Rust desktop app at ../../candybar/trunk-main) for real-time Bloodbank event monitoring and tracing.

### User Needs

1. Trust that schemas are current and accurate (single source of truth)
2. Fast validation (< S effort to check contract compliance)
3. Clear breaking change notifications (caught in CI before runtime)

---

## Solution Overview

### Proposed Solution

bloodbank-contracts as a centralized event schema registry using JSON Schema as source of truth, with automated generation of language-specific artifacts (Python Pydantic, TypeScript Zod/types, future Rust serde structs). Contract validation integrated into component CI pipelines catches violations before runtime. Per-component semantic versioning enables parallel development without coordination bottlenecks.

### Key Features

- Event Schema Storage: JSON Schema definitions as single source of truth
- Multi-language Code Generation: Automated Pydantic (Python), Zod/types (TypeScript), serde (Rust future)
- Contract Test Suites: Schema conformance validation (not integration tests)
- Version Management: Per-component semantic versioning for maximum flexibility
- Documentation: Human-readable event catalog with usage examples
- CI/CD Integration: Pre-commit linting and GitHub Actions validation
- Breaking Change Detection: Automated detection of contract violations

### Value Proposition

Faster iteration without cross-repo coordination wait times. Lower risk through contract violations caught in CI before runtime. Better agent autonomy with clear contracts requiring less human intervention.

---

## Business Objectives

### Goals

- Increase development velocity: Reduce cross-repo coordination overhead
- Enable agent autonomy: Claude agents develop independently with contract guarantees
- Support ecosystem scalability: Add new components without geometric complexity growth

### Success Metrics

- Contract test coverage: Track percentage of events with validation tests
- Breaking changes caught in CI: Target 100% detection before runtime
- Time to onboard new service: Measure from component creation to contract validation

### Business Value

Faster iteration through elimination of manual coordination. Higher quality through automated contract enforcement. Lower cognitive load as contracts replace mental coordination models.

---

## Scope

### In Scope

- Schema definition infrastructure (JSON Schema as source of truth)
- Generated artifacts for Python and TypeScript (v1), Rust (future)
- Per-component semantic versioning
- Pre-commit linting (schema structure validation)
- Contract test suites (schema conformance, not integration behavior)
- GitHub Actions for contract validation and breaking change detection
- Automated artifact generation on schema changes
- Usage examples per command/event
- Human-readable event catalog
- Migration guides for breaking changes
- Initial components: common/ (base types, enums), theboard/ (commands + events), theboardroom/ (events, consumer-side)

### Out of Scope

- Runtime validation libraries in consuming services
- Event routing logic or Bloodbank client wrappers
- Monitoring/tracing instrumentation
- Migration tooling for schema evolution
- CLI tools for schema generation/validation
- Auto-discovery or registry service

### Future Considerations

- Additional component contracts (Flume, Holocene, iMi, Jelmore, 00_ceiling, Yi, Zellij-driver, Candybar)
- Schema migration tooling (auto-upgrade consumers)
- Contract registry service (runtime schema lookup, referenced at ../../services)
- Observability hooks (contract violation telemetry)
- Multi-version compatibility layer

---

## Key Stakeholders

- **Jarad DeLorenzo (Developer/Orchestrator)** - High. Direct implementer, owns architecture decisions for 33GOD ecosystem.
- **LLM Coding Agents (Claude instances on components)** - High. Primary consumers who depend on contracts for coordination and independent development.
- **Future Letta Director Agent** - Medium. Will orchestrate cross-repo workflows and needs contract visibility for coordination.
- **CI/CD Systems (GitHub Actions)** - Low. Enforces contract validation but doesn't shape requirements.

---

## Constraints and Assumptions

### Constraints

No major constraints identified. Project uses existing infrastructure (GitHub, RabbitMQ/Bloodbank, uv/bun package managers) without additional budget or tooling requirements.

### Assumptions

- Claude agents can parse and validate JSON Schema
- RabbitMQ/Bloodbank infrastructure is stable and available
- Components will adopt contract validation in their CI pipelines
- GitHub Actions has sufficient compute resources for contract test execution
- JSON Schema generation toolchain (datamodel-code-generator, json-schema-to-zod, typify) is mature enough for production use

---

## Success Criteria

- Claude agents stop encountering schema mismatch errors during development
- All new 33GOD components start with contract definition first (contract-driven development)
- Zero runtime event parsing failures in production for events with defined contracts
- Can add new component contracts in < M effort without cross-repo coordination
- Developers have confidence to refactor services without fear of breaking consumers

---

## Timeline and Milestones

### Target Launch

Unblock TheBoard/TheBoardroom integration as priority. Get walking skeleton deployed within M effort (schema infrastructure + initial contracts + CI validation).

### Key Milestones

1. Schema infrastructure setup (JSON Schema, generation toolchain)
2. TheBoard contracts defined (commands + events)
3. Contract tests passing in CI
4. TheBoard/TheBoardroom integration validated
5. Documentation complete

---

## Risks and Mitigation

- **Risk:** Schema generation complexity - tooling gaps for Python/TypeScript/Rust generation
  - **Likelihood:** Medium
  - **Mitigation:** Start with Python only (Pydantic exports JSON Schema), add TypeScript when TheBoard/TheBoardroom integration validated, defer Rust until Candybar needs it. Reversible and lower risk.

- **Risk:** Adoption resistance - components don't integrate contract validation into CI
  - **Likelihood:** Low
  - **Mitigation:** Start with TheBoard/TheBoardroom as reference implementation. Make CI integration straightforward with clear examples and pre-commit hooks.

- **Risk:** Contract staleness - PRD entropy problem extends to contracts (schemas drift from reality)
  - **Likelihood:** Medium
  - **Mitigation:** Contract tests in component CI will fail if implementation drifts from contracts. Breaking change detection provides fast feedback loop.

- **Risk:** False confidence - contract tests pass but integration still fails at runtime
  - **Likelihood:** Low
  - **Mitigation:** Contract tests validate schema structure only (in scope). Integration tests remain responsibility of component repos. Clear documentation of test boundaries prevents misunderstanding.

- **Risk:** Multi-language maintenance burden - keeping 3 language targets in sync
  - **Likelihood:** Medium
  - **Mitigation:** Automated generation from JSON Schema single source of truth. Generation happens in CI, not manually. Start with 2 languages (Python + TypeScript), add Rust when proven necessary.

---

## Next Steps

1. Create Technical Specification - `/tech-spec`
2. Define schema infrastructure and generation toolchain
3. Begin TheBoard contract definitions

---

**This document was created using BMAD Method v6 - Phase 1 (Analysis)**

*To continue: Run `/workflow-status` to see your progress and next recommended workflow.*

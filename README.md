# Holyfields

Event schema registry and contract system for the 33GOD ecosystem.

## Overview

Holyfields provides a single source of truth for event schemas shared across 33GOD microservices. It auto-generates language-specific artifacts (Python Pydantic, TypeScript Zod) from JSON Schema definitions, enabling independent component development with guaranteed schema compatibility.

## Problem Solved

When developing TheBoard (Python backend) and TheBoardroom (TypeScript frontend) in parallel, event schema mismatches caused silent failures, missing UI updates, and fake mocked behavior. Holyfields catches these at build time through contract validation.

## Quick Start

```bash
# Install dependencies
mise run install

# Validate schemas
mise run validate:schemas

# Generate all language artifacts
mise run generate:all

# Run contract tests
mise run test:all

# Full CI validation
mise run ci
```

## Directory Structure

```
holyfields/
├── common/schemas/          # Shared base types and enums
├── theboard/               # TheBoard component contracts
│   ├── events/            # Event schemas (immutable)
│   └── commands/          # Command schemas (mutable)
├── theboardroom/          # TheBoardroom component contracts
│   └── events/            # Consumer-side event schemas
├── generated/             # Auto-generated language artifacts
│   ├── python/           # Pydantic models
│   └── typescript/       # Zod schemas + TS types
├── tests/                # Contract validation tests
│   ├── python/          # pytest suites
│   └── typescript/      # vitest suites
├── docs/                # Documentation
│   ├── catalog/        # Per-event docs
│   ├── guides/         # Integration guides
│   └── integration-tickets/  # Cross-repo coordination tickets
└── scripts/            # Generation + validation scripts
```

## Schema Definition

Schemas are defined in JSON Schema Draft 2020-12 format:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://33god.dev/schemas/theboard/events/meeting_created.json",
  "type": "object",
  "title": "Meeting Created Event",
  "description": "Emitted when a new meeting is created",
  "properties": {
    "event_type": {
      "type": "string",
      "const": "theboard.meeting.created"
    },
    "meeting_id": {
      "type": "string",
      "format": "uuid"
    },
    "topic": {
      "type": "string",
      "description": "Meeting topic/question"
    }
  },
  "required": ["event_type", "meeting_id", "topic"]
}
```

## Code Generation

### Python (Pydantic)

```bash
mise run generate:python
```

Generates type-safe Pydantic models in `generated/python/`:

```python
from generated.python.theboard.events import MeetingCreatedEvent

event = MeetingCreatedEvent(
    event_type="theboard.meeting.created",
    meeting_id="...",
    topic="AI safety"
)
```

### TypeScript (Zod)

```bash
mise run generate:typescript
```

Generates Zod schemas and TypeScript types in `generated/typescript/`:

```typescript
import { MeetingCreatedEventSchema } from './generated/typescript/theboard/events';

const event = MeetingCreatedEventSchema.parse(rawData);
```

## Contract Validation

Contract tests ensure generated artifacts match schema expectations:

```bash
# Python tests
mise run test:python

# TypeScript tests
mise run test:typescript

# All tests
mise run test:all
```

## Versioning

Each component directory uses independent semantic versioning:

- **Major**: Breaking changes (field removal, type change)
- **Minor**: Additive changes (new optional field)
- **Patch**: Documentation/comment changes

Version tracked in component metadata file (e.g., `theboard/version.json`).

## Integration Workflow

1. **Define Schema**: Add/modify JSON Schema in component directory
2. **Validate**: Pre-commit hook validates schema structure
3. **Generate**: CI generates Python and TypeScript artifacts
4. **Test**: Contract tests validate generated code
5. **Consume**: Dependent services import generated artifacts

## Cross-Repo Coordination

For changes affecting external teams (like theboard), see:

- `docs/integration-tickets/` - Detailed tickets for external teams
- Each ticket includes schema changes, migration guide, and acceptance criteria

## CI Integration

GitHub Actions workflow (`ci validate-contracts.yml`) runs on every PR:

- Schema validation
- Code generation
- Contract tests
- Breaking change detection

## Tech Stack

- **Schema Format**: JSON Schema Draft 2020-12
- **Python Generation**: datamodel-code-generator
- **TypeScript Generation**: json-schema-to-zod
- **Python Validation**: jsonschema + pytest
- **TypeScript Validation**: ajv + vitest
- **Task Runner**: mise
- **Package Managers**: uv (Python), bun (TypeScript)

## Current Components

- **common/**: Base types, enums, shared structures
- **theboard/**: Meeting orchestration events (7 events)
- **theboardroom/**: Visualization consumer events

## Future Components

- flume/
- holocene/
- imi/
- jelmore/
- 00_ceiling/
- yi/
- zellij-driver/
- candybar/

## Contributing

1. Define schema in appropriate component directory
2. Run `mise run validate:schemas`
3. Run `mise run generate:all`
4. Run `mise run test:all`
5. Commit schema + generated artifacts
6. CI validates on PR

## Related Documentation

- [Product Brief](docs/product-brief-holyfields-2026-01-14.md)
- [Technical Specification](docs/tech-spec-holyfields-2026-01-14.md)
- [Sprint Plan](docs/sprint-plan-holyfields-2026-01-14.md)
- [Event Catalog](docs/catalog/) (per-event documentation)

## Project Status

- **Version**: 0.1.0
- **Status**: In Development (Sprint 1)
- **Target**: Unblock TheBoard/TheBoardroom integration

## Contact

Jarad DeLorenzo - 33GOD Ecosystem

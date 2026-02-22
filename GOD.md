# Holyfields — GOD Document

> **Guaranteed Organizational Document** — Developer-facing reference for Holyfields
>
> **Last Updated**: 2026-02-22
> **Domain**: Infrastructure
> **Status**: Production
> **Owner**: Lenoon 🦎 (agent:infra)

---

## Product Overview

**Holyfields** is the **canonical schema registry** for the 33GOD ecosystem. It is the **single source of truth** for all event definitions, type contracts, and data structures that flow through Bloodbank. Every event that traverses the 33GOD pipeline is defined here first—**no exceptions**.

**Core Purpose:**
- Define **all event schemas** in one authoritative location
- Generate **type-safe bindings** for Python (Pydantic) and TypeScript (Zod)
- Enforce **contract consistency** across producers and consumers
- Enable **schema evolution** with versioning and migration paths

**Why Holyfields Exists:**
In an event-driven architecture, the schema IS the contract. Holyfields eliminates the "implicit contract" anti-pattern where producers and consumers assume they understand the same data structure. If it's not in Holyfields, it doesn't exist in the 33GOD ecosystem.

---

## Architecture Position

Holyfields sits at the **foundation** of the 33GOD event flow:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HOLYFIELDS (Definition)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Event Schemas│  │ Type Bindings│  │  Contracts   │  │  Versions    │     │
│  │   (JSON)     │  │(Python/TS)   │  │   (Docs)     │  │  (SemVer)    │     │
│  └──────┬───────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────┼────────────────────────────────────────────────────────────────────┘
          │
          ▼ Defines
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BLOODBANK (Transport)                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │              RabbitMQ Exchange: bloodbank.events.v1                  │    │
│  │                    (TOPIC, Durable)                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
          │
          ▼ Persists
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CANDYSTORE (Persistence)                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │              PostgreSQL Event Store (Permanent History)              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
          │
          ▼ Queries
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HOLOCENE (Visibility)                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │    Real-Time Dashboard (Candystore API + WS Relay)                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
          │
          ▼ Consumes
┌─────────────────────────────────────────────────────────────────────────────┐
│                      HEARTBEATROUTER / AGENTS (Action)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Heartbeat Tick│  │ Agent Inbox  │  │  Task Exec   │  │  System Ops  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**The Golden Rule:**
```
Holyfields (Schema) → Bloodbank (Event) → Candystore (History) → Holocene (View) → Agents (Action)
```

No component may emit or consume an event that is not defined in Holyfields. This is non-negotiable.

---

## Directory Structure

```
holyfields/
├── schemas/                      # Canonical JSON Schema definitions
│   ├── _common/                  # Shared base types (envelope, source, etc.)
│   │   └── event-envelope.json   # Base envelope all events extend
│   ├── agent/                    # Agent domain events
│   │   ├── agent-task-created.json
│   │   ├── agent-task-claimed.json
│   │   ├── agent-task-completed.json
│   │   └── agent-status-update.json
│   ├── system/                   # System-level events
│   │   ├── system-heartbeat-tick.json
│   │   └── system-health-check.json
│   ├── webhook/                  # Webhook integration events
│   │   └── webhook-plane-issue-updated.json
│   └── [domain]/                 # Other domain events
│
├── python/                       # Generated Python bindings
│   └── holyfields/
│       ├── __init__.py
│       ├── common.py             # EventEnvelope, Source, etc.
│       ├── agent.py              # Agent event models
│       ├── system.py             # System event models
│       └── webhook.py            # Webhook event models
│
├── typescript/                   # Generated TypeScript bindings
│   └── src/
│       ├── common.ts             # EventEnvelope, Source, etc.
│       ├── agent.ts              # Agent event types
│       ├── system.ts             # System event types
│       └── webhook.ts            # Webhook event types
│
├── docs/                         # Human-readable schema documentation
│   └── README.md                 # Schema catalog and usage guide
│
├── Makefile                      # Code generation commands
└── pyproject.toml                # Python package config
```

---

## Event Schema Definition

### Schema Structure

Every event schema in Holyfields follows this structure:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://33god.dev/schemas/[domain]/[event-name].json",
  "title": "[EventName]",
  "description": "Human-readable description of when this event fires",
  "type": "object",
  "allOf": [
    { "$ref": "../_common/event-envelope.json" }
  ],
  "properties": {
    "event_type": {
      "type": "string",
      "const": "[domain].[resource].[action]"
    },
    "payload": {
      "type": "object",
      "properties": {
        // Event-specific properties here
      },
      "required": ["..."]
    }
  },
  "required": ["event_type", "payload"]
}
```

### Example: System Heartbeat Tick

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://33god.dev/schemas/system/heartbeat-tick.json",
  "title": "SystemHeartbeatTick",
  "description": "Fired every 60 seconds to trigger agent heartbeat processing",
  "type": "object",
  "allOf": [
    { "$ref": "../_common/event-envelope.json" }
  ],
  "properties": {
    "event_type": {
      "type": "string",
      "const": "system.heartbeat.tick"
    },
    "payload": {
      "type": "object",
      "properties": {
        "tick_id": {
          "type": "string",
          "format": "uuid",
          "description": "Unique identifier for this tick"
        },
        "sequence_number": {
          "type": "integer",
          "description": "Monotonically increasing tick counter"
        },
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 timestamp of tick generation"
        }
      },
      "required": ["tick_id", "sequence_number", "timestamp"]
    }
  },
  "required": ["event_type", "payload"]
}
```

### Example: Agent Task Created

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://33god.dev/schemas/agent/task-created.json",
  "title": "AgentTaskCreated",
  "description": "Emitted when a new task is assigned to an agent",
  "type": "object",
  "allOf": [
    { "$ref": "../_common/event-envelope.json" }
  ],
  "properties": {
    "event_type": {
      "type": "string",
      "const": "agent.task.created"
    },
    "payload": {
      "type": "object",
      "properties": {
        "task_id": { "type": "string", "format": "uuid" },
        "agent_name": { "type": "string" },
        "task_type": { 
          "type": "string",
          "enum": ["code", "review", "research", "document", "test"]
        },
        "description": { "type": "string" },
        "priority": {
          "type": "string",
          "enum": ["low", "medium", "high", "critical"]
        },
        "due_at": { "type": "string", "format": "date-time" },
        "correlation_id": { "type": "string" }
      },
      "required": ["task_id", "agent_name", "task_type", "description"]
    }
  },
  "required": ["event_type", "payload"]
}
```

---

## Event Envelope (Base Type)

All events in 33GOD extend the **EventEnvelope** base schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://33god.dev/schemas/_common/event-envelope.json",
  "title": "EventEnvelope",
  "description": "Base envelope for all 33GOD events",
  "type": "object",
  "properties": {
    "event_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this event instance"
    },
    "event_type": {
      "type": "string",
      "description": "Event type in domain.resource.action format",
      "pattern": "^[a-z0-9]+\\.[a-z0-9]+\\.[a-z0-9]+(\\.[a-z0-9]+)*$"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when event was created"
    },
    "version": {
      "type": "string",
      "description": "Schema version (SemVer)",
      "default": "1.0.0"
    },
    "source": {
      "type": "object",
      "properties": {
        "host": { "type": "string", "description": "Machine hostname" },
        "app": { "type": "string", "description": "Application/service name" },
        "type": {
          "type": "string",
          "enum": ["agent", "system", "cron", "webhook", "user"],
          "description": "Type of event source"
        }
      },
      "required": ["host", "app", "type"]
    },
    "payload": {
      "type": "object",
      "description": "Event-specific data"
    },
    "correlation_id": {
      "type": "string",
      "description": "Links related events across the system"
    },
    "session_id": {
      "type": "string",
      "description": "Groups events within a user/agent session"
    },
    "routing_key": {
      "type": "string",
      "description": "RabbitMQ routing key (auto-set by Bloodbank)"
    }
  },
  "required": ["event_id", "event_type", "timestamp", "version", "source", "payload"]
}
```

---

## Immutability vs Mutability

### Events are Immutable

**Events** represent facts that have occurred. They are:
- **Appended** to the event log (never modified)
- **Triggered** by state changes
- **Consumed** by interested parties
- **Never deleted** (permanent history in Candystore)

Examples:
- `agent.task.created` — A task was created. Fact.
- `system.heartbeat.tick` — A heartbeat occurred. Fact.
- `worktree.merged` — Code was merged. Fact.

### Commands are Mutable

**Commands** represent requests for action. They are:
- **Fired** to request state changes
- **May be rejected** (unlike events which are facts)
- **Idempotent** when possible (same command multiple times = same result)
- **Processed** by handlers that may emit events

Examples:
- `agent.task.assign` — Request to assign a task (may fail if agent busy)
- `worktree.create` — Request to create a worktree (may fail if exists)
- `session.end` — Request to end a session (may fail if already ended)

### Event Naming Conventions

| Pattern | Type | Example |
|---------|------|---------|
| `[domain].[resource].[past-tense-verb]` | Event | `agent.task.completed` |
| `[domain].[resource].[imperative-verb]` | Command | `agent.task.complete` |
| `system.[component].[action]` | System Event | `system.heartbeat.tick` |
| `webhook.[source].[action]` | Webhook Event | `webhook.plane.issue.updated` |

---

## Code Generation

### Python Bindings

Generate Pydantic models from JSON schemas:

```bash
cd holyfields
make generate-python
```

This creates type-safe Pydantic models:

```python
from holyfields.system import SystemHeartbeatTick
from holyfields.agent import AgentTaskCreated

# Type-safe event construction
heartbeat = SystemHeartbeatTick(
    event_id="uuid-here",
    event_type="system.heartbeat.tick",
    timestamp="2026-02-22T18:30:00Z",
    source={"host": "big-chungus", "app": "bloodbank", "type": "system"},
    payload={
        "tick_id": "tick-123",
        "sequence_number": 42,
        "timestamp": "2026-02-22T18:30:00Z"
    }
)

# Validation happens automatically
heartbeat.payload.sequence_number  # int
heartbeat.payload.invalid_field    # AttributeError!
```

### TypeScript Bindings

Generate Zod schemas from JSON schemas:

```bash
cd holyfields
make generate-typescript
```

This creates Zod validators:

```typescript
import { SystemHeartbeatTick, AgentTaskCreated } from '@33god/holyfields';

// Runtime validation
const result = SystemHeartbeatTick.safeParse(eventData);
if (result.success) {
  result.payload.sequence_number; // Typed as number
}
```

---

## Schema Versioning

### Semantic Versioning

Holyfields uses SemVer for schema versions:

- **MAJOR**: Breaking changes (renamed fields, removed properties)
- **MINOR**: Additive changes (new optional fields)
- **PATCH**: Documentation fixes, constraint relaxations

### Migration Strategy

When evolving schemas:

1. **Create new version** in `schemas/v2/...` for breaking changes
2. **Update version** field in schema (`"version": "2.0.0"`)
3. **Maintain consumers** during transition period
4. **Deprecate old** after all consumers updated
5. **Remove old** after deprecation period

### Compatibility Guarantees

- **Minor/Patch versions**: Always backward compatible
- **Major versions**: May require consumer updates
- **Deprecation window**: 30 days minimum for major changes

---

## Critical Event Catalog

### System Events

| Event Type | Schema | Description |
|------------|--------|-------------|
| `system.heartbeat.tick` | `system/heartbeat-tick.json` | 60-second heartbeat pulse |
| `system.health.check` | `system/health-check.json` | Service health status |
| `system.component.started` | `system/component-started.json` | Service initialization |
| `system.component.stopped` | `system/component-stopped.json` | Service shutdown |

### Agent Events

| Event Type | Schema | Description |
|------------|--------|-------------|
| `agent.task.created` | `agent/task-created.json` | Task assigned to agent |
| `agent.task.claimed` | `agent/task-claimed.json` | Agent accepted task |
| `agent.task.progress` | `agent/task-progress.json` | Progress update |
| `agent.task.completed` | `agent/task-completed.json` | Task finished |
| `agent.status.update` | `agent/status-update.json` | Agent availability change |
| `agent.message.received` | `agent/message-received.json` | Message to agent inbox |

### Workspace Events

| Event Type | Schema | Description |
|------------|--------|-------------|
| `worktree.created` | `worktree/created.json` | New worktree allocated |
| `worktree.claimed` | `worktree/claimed.json` | Agent claimed worktree |
| `worktree.released` | `worktree/released.json` | Agent released worktree |
| `worktree.merged` | `worktree/merged.json` | Worktree merged to trunk |

### Webhook Events

| Event Type | Schema | Description |
|------------|--------|-------------|
| `webhook.plane.issue.created` | `webhook/plane-issue-created.json` | New Plane ticket |
| `webhook.plane.issue.updated` | `webhook/plane-issue-updated.json` | Ticket modified |
| `webhook.github.pr.opened` | `webhook/github-pr-opened.json` | Pull request opened |
| `webhook.github.push` | `webhook/github-push.json` | Code pushed |

---

## Development Workflow

### Adding a New Event

1. **Define schema** in `schemas/[domain]/[event-name].json`
2. **Reference base envelope** via `$ref`
3. **Set event_type const** matching filename
4. **Document payload fields** with descriptions
5. **Generate bindings**: `make generate`
6. **Test validation**: Ensure consumers can parse
7. **Update docs**: Add to Critical Event Catalog

### Schema Review Checklist

- [ ] Event type follows naming convention
- [ ] All fields have descriptions
- [ ] Required fields marked
- [ ] UUIDs use `format: "uuid"`
- [ ] Timestamps use `format: "date-time"`
- [ ] Enums are explicit (no free-form strings)
- [ ] Base envelope extended correctly
- [ ] Version specified

---

## Integration Points

### For Bloodbank

Bloodbank validates events against Holyfields schemas (planned). Currently, validation is loose—producers are trusted to conform.

### For Candystore

Candystore persists all events. The `payload` field is stored as JSONB for query flexibility while maintaining envelope structure.

### For Holocene

Holocene uses Holyfields TypeScript bindings for type-safe event consumption in the frontend.

### For Agents

Agents import Holyfields Python bindings for type-safe event publishing and consumption.

---

## References

- **System Doc**: `~/code/33GOD/docs/GOD.md`
- **Bloodbank Doc**: `~/code/33GOD/bloodbank/GOD.md`
- **Candystore Doc**: `~/code/33GOD/candystore/GOD.md`
- **Domain Doc**: `~/code/33GOD/docs/domains/infrastructure/GOD.md`
- **Schema Directory**: `~/code/33GOD/holyfields/schemas/`

---

## Maintenance

This document is updated when:
- New event schemas are added
- Schema structure changes
- Code generation process changes
- Versioning policy updates

**Last comprehensive review**: 2026-02-22

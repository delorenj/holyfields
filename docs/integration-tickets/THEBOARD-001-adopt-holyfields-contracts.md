# THEBOARD-001: Adopt Holyfields Event Contracts

**Priority**: High
**Estimation**: 8 Story Points
**Team**: theboard
**Dependencies**: None
**Blocked By**: None

## User Story

As a theboard developer, I want to migrate from hand-written Pydantic schemas to Holyfields-generated contracts so that event schemas are automatically synchronized with downstream consumers like theboardroom.

## Background

Currently, theboard maintains event schemas in `src/theboard/events/schemas.py` as Pydantic models. This creates several problems:

1. **Schema Drift**: theboardroom expects events that theboard doesn't emit (participant.added, participant.turn_started, participant.turn_completed)
2. **Manual Synchronization**: Changes to event schemas require manual updates in multiple repos
3. **Runtime Failures**: Mismatched schemas cause runtime errors that could be caught at build time
4. **No Contract Enforcement**: No automated validation that published events match expected schemas

**Holyfields** is a new centralized contract system that:
- Maintains JSON Schema as single source of truth
- Generates Pydantic models for Python services (like theboard)
- Generates Zod schemas for TypeScript services (like theboardroom)
- Provides validation and testing frameworks

## Acceptance Criteria

- [ ] Replace hand-written Pydantic classes in `src/theboard/events/schemas.py` with generated models from Holyfields
- [ ] Add Holyfields as a dependency in `pyproject.toml`
- [ ] Configure import path to use `from holyfields.generated.python.theboard.events import *`
- [ ] All existing event emissions work unchanged (7 events: created, started, round_completed, comment_extracted, converged, completed, failed)
- [ ] All unit tests pass without modification
- [ ] Update developer documentation to reference Holyfields contract source
- [ ] Create pre-commit hook to regenerate contracts on schema changes (future-proofing)

## Technical Implementation Notes

### Current State
```python
# src/theboard/events/schemas.py
from pydantic import BaseModel, Field

class BaseEvent(BaseModel):
    model_config = {"frozen": True}
    event_type: str
    timestamp: datetime
    meeting_id: UUID

class MeetingCreatedEvent(BaseEvent):
    event_type: Literal["meeting.created"] = "meeting.created"
    topic: str
    strategy: str
    max_rounds: int
    agent_count: int | None = None
```

### Target State
```python
# src/theboard/events/schemas.py
"""Event schemas for TheBoard - GENERATED FROM HOLYFIELDS.

DO NOT EDIT MANUALLY. Source schemas at:
~/code/33GOD/holyfields/trunk-main/theboard/events/*.json

To regenerate: cd ~/code/33GOD/holyfields/trunk-main && mise run generate:python
"""

from holyfields.generated.python.theboard.events import (
    MeetingCreatedEvent,
    MeetingStartedEvent,
    RoundCompletedEvent,
    CommentExtractedEvent,
    MeetingConvergedEvent,
    MeetingCompletedEvent,
    MeetingFailedEvent,
)

__all__ = [
    "MeetingCreatedEvent",
    "MeetingStartedEvent",
    "RoundCompletedEvent",
    "CommentExtractedEvent",
    "MeetingConvergedEvent",
    "MeetingCompletedEvent",
    "MeetingFailedEvent",
]
```

### Installation Steps

1. **Add Holyfields dependency**:
```toml
# pyproject.toml
[project]
dependencies = [
    # ... existing deps
    "holyfields @ file:///home/delorenj/code/33GOD/holyfields/trunk-main",
]
```

2. **Generate Pydantic models** (do once initially):
```bash
cd ~/code/33GOD/holyfields/trunk-main
mise run generate:python  # Generates to generated/python/
```

3. **Replace imports** in theboard codebase:
```bash
# Find all imports of event schemas
rg "from theboard.events.schemas import" --files-with-matches

# Update each file to import from holyfields instead
```

4. **Run tests**:
```bash
cd ~/code/33GOD/theboard/trunk-main
pytest tests/events/  # Should pass without changes
```

### Migration Checklist

Files that import event schemas (need import updates):
- `src/theboard/core/meeting.py` - MeetingOrchestrator emits events
- `src/theboard/services/notetaker.py` - Emits CommentExtractedEvent
- `src/theboard/events/emitter.py` - Event emission logic
- `tests/events/test_schemas.py` - Schema validation tests
- Any other files found via `rg "from.*schemas import"`

### Breaking Changes

**None expected**. Generated Pydantic models have identical structure to hand-written ones. All field names, types, and defaults match exactly.

### Testing Strategy

1. **Unit tests**: Existing tests in `tests/events/` should pass unchanged
2. **Integration tests**: Run sample meeting with event emission to verify runtime behavior
3. **Schema validation**: Use `mise run validate:schemas` in Holyfields to validate all 7 event types
4. **Regression testing**: Compare event payloads before/after migration (should be identical)

## Risk Assessment

**Low Risk**. This is primarily a refactoring of import paths. The generated schemas are functionally identical to the hand-written ones.

**Rollback Plan**: If issues arise, revert to original `schemas.py` file (keep backup during migration).

## Documentation Updates

Update the following docs:
- `docs/events.md` - Add section explaining Holyfields contract system
- `docs/development.md` - Add instructions for regenerating contracts when schemas change
- `README.md` - Add Holyfields setup to development environment instructions

## Related Tickets

- **THEBOARD-002**: Add missing participant turn events (requires Holyfields adoption first)
- **THEBOARD-003**: Migration guide for other services adopting Holyfields

## Definition of Done

- [ ] All acceptance criteria met
- [ ] All tests passing (existing + new)
- [ ] Code review approved
- [ ] Documentation updated
- [ ] Changes merged to main branch
- [ ] theboardroom team notified of contract availability

## Questions for Product Owner

1. Should we create a mise task in theboard repo that auto-syncs with Holyfields, or rely on manual regeneration?
2. Do we want CI to validate that committed code uses latest Holyfields contracts?

## External Team Contact

**Owner**: Holyfields Team
**Point of Contact**: @developer (this agent)
**Support Channel**: Holyfields repo issues

For questions about:
- Schema format or structure → Check Holyfields `docs/schema-guide.md`
- Generation failures → Check Holyfields `docs/troubleshooting.md`
- New event types → Create PR in Holyfields repo first, then regenerate in theboard

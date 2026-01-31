# THEBOARD-003: Create Holyfields Migration Guide

**Priority**: Medium
**Estimation**: 3 Story Points
**Team**: theboard
**Dependencies**: THEBOARD-001 (Adopt Holyfields Contracts)
**Blocked By**: THEBOARD-001

## User Story

As a theboard developer, I want a comprehensive migration guide so that I can confidently refactor event emission code to use Holyfields contracts and understand how to add new event types in the future.

## Background

THEBOARD-001 covers the mechanical steps of adopting Holyfields (changing imports, adding dependencies). This ticket covers creating documentation for:

1. **Developer onboarding**: How new team members understand the contract system
2. **Event lifecycle**: How to add/modify/deprecate event schemas
3. **Troubleshooting**: Common issues during migration and how to fix them
4. **Best practices**: Patterns for event design and emission

## Acceptance Criteria

- [ ] Create `docs/holyfields-migration-guide.md` with step-by-step migration instructions
- [ ] Document event lifecycle (schema creation → generation → emission → consumption)
- [ ] Add troubleshooting section with common issues and solutions
- [ ] Create examples of adding a new event type end-to-end
- [ ] Document rollback procedure if migration causes issues
- [ ] Add pre-commit hook instructions for automatic contract regeneration
- [ ] Create comparison table: Before (hand-written Pydantic) vs After (Holyfields-generated)
- [ ] Link from main README.md to migration guide

## Technical Implementation Notes

### Document Structure

**File**: `docs/holyfields-migration-guide.md`

```markdown
# Holyfields Migration Guide for theboard

## Overview
Why we migrated, benefits, scope of changes

## Quick Start
For developers who just need to get going

## Understanding Holyfields
High-level architecture of the contract system

## Migration Steps
Step-by-step instructions for adopting contracts

## Event Lifecycle
How events flow from schema → code → emission → consumption

## Adding New Event Types
End-to-end walkthrough with examples

## Modifying Existing Events
Breaking vs non-breaking changes

## Troubleshooting
Common issues and solutions

## Best Practices
Event design patterns and anti-patterns

## FAQ
Answers to common questions
```

### Key Sections to Include

#### 1. Before/After Comparison

```python
# BEFORE: Hand-written Pydantic in schemas.py
class MeetingCreatedEvent(BaseEvent):
    event_type: Literal["meeting.created"] = "meeting.created"
    topic: str
    strategy: str
    max_rounds: int

# AFTER: Generated from Holyfields
from holyfields.generated.python.theboard.events import MeetingCreatedEvent
# Functionally identical, but source of truth is JSON Schema
```

#### 2. Event Lifecycle Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Define Schema (holyfields/theboard/events/*.json)       │
│    - JSON Schema Draft 2020-12                              │
│    - Extends common/schemas/base_event.json                 │
│    - Uses $ref for type reuse                               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Generate Code (mise run generate:python)                │
│    - datamodel-code-generator creates Pydantic models       │
│    - Output: generated/python/theboard/events/*.py          │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Import in theboard (from holyfields.generated...)       │
│    - Replace hand-written schemas with generated imports   │
│    - No code logic changes required                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Emit Events (event_emitter.emit(Event(...)))            │
│    - Same emission code as before                           │
│    - Pydantic validation automatically applied              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Consume Events (theboardroom, other services)           │
│    - TypeScript consumers use generated Zod schemas         │
│    - Python consumers use generated Pydantic models         │
│    - Contract guarantees compatibility                      │
└─────────────────────────────────────────────────────────────┘
```

#### 3. Adding a New Event Type

**Example: Adding a `participant.voted` event**

```bash
# Step 1: Create JSON Schema in Holyfields repo
cd ~/code/33GOD/holyfields/trunk-main
cat > theboard/events/participant_voted.json <<'EOF'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://33god.dev/schemas/theboard/events/participant_voted.json",
  "title": "Participant Voted Event",
  "description": "Emitted when participant votes on a comment or proposal.",
  "type": "object",
  "allOf": [{"$ref": "../../common/schemas/base_event.json"}],
  "properties": {
    "event_type": {
      "type": "string",
      "const": "participant.voted"
    },
    "agent_name": {
      "$ref": "../../common/schemas/types.json#/$defs/agent_name"
    },
    "vote_type": {
      "type": "string",
      "enum": ["upvote", "downvote", "abstain"]
    },
    "target_comment_id": {
      "type": "string",
      "format": "uuid"
    }
  },
  "required": ["event_type", "timestamp", "meeting_id", "agent_name", "vote_type", "target_comment_id"]
}
EOF

# Step 2: Validate schema
mise run validate:schemas

# Step 3: Generate Pydantic models
mise run generate:python

# Step 4: Update theboard imports
cd ~/code/33GOD/theboard/trunk-main
# Edit src/theboard/events/schemas.py to add:
from holyfields.generated.python.theboard.events import (
    # ... existing imports
    ParticipantVotedEvent,  # ADD THIS
)

# Step 5: Emit event in theboard code
# In src/theboard/core/voting.py (example):
self.event_emitter.emit(
    ParticipantVotedEvent(
        meeting_id=self.meeting_id,
        agent_name=voter.name,
        vote_type="upvote",
        target_comment_id=comment.id
    )
)

# Step 6: Test
pytest tests/events/test_voting_events.py

# Step 7: Notify consumers
# Update docs/events.md with new event type
# Create integration ticket for theboardroom if they need to consume it
```

#### 4. Troubleshooting Common Issues

**Issue 1: Import error after regeneration**
```python
# Error: ModuleNotFoundError: No module named 'holyfields.generated.python'

# Solution: Ensure Holyfields package is installed
cd ~/code/33GOD/holyfields/trunk-main
uv pip install -e .

# Or in theboard's pyproject.toml:
dependencies = [
    "holyfields @ file:///home/delorenj/code/33GOD/holyfields/trunk-main",
]
```

**Issue 2: Validation error on event emission**
```python
# Error: ValidationError: 1 validation error for MeetingCreatedEvent
#   topic
#     field required (type=value_error.missing)

# Solution: Check schema requirements match emission code
# Schema requires 'topic' but code didn't provide it
event = MeetingCreatedEvent(
    meeting_id=uuid4(),
    topic="My Topic",  # ADD MISSING FIELD
    strategy="multi_agent",
    max_rounds=5
)
```

**Issue 3: Generated code out of sync with schemas**
```python
# Error: Event has unexpected field 'new_field'

# Solution: Regenerate contracts after schema changes
cd ~/code/33GOD/holyfields/trunk-main
mise run generate:python
cd ~/code/33GOD/theboard/trunk-main
# Restart dev server / re-import package
```

#### 5. Best Practices

**DO**:
- ✅ Always validate schemas before generation (`mise run validate:schemas`)
- ✅ Use `$ref` for shared types (agent_name, round_number, etc.)
- ✅ Add clear descriptions to all schema properties
- ✅ Provide examples in schema files
- ✅ Emit events at logical boundaries (before/after state transitions)
- ✅ Include enough context in events for downstream consumers to act independently

**DON'T**:
- ❌ Modify generated Python files directly (they'll be overwritten)
- ❌ Create events with mutable payloads (events are immutable by design)
- ❌ Emit events that duplicate information already in other events
- ❌ Add breaking changes to existing events (use schema versioning instead)
- ❌ Skip validation (`mise run validate:schemas`) before committing schema changes

#### 6. Breaking vs Non-Breaking Changes

**Non-Breaking** (safe to deploy):
- Adding optional fields to existing events
- Adding new event types
- Adding enum values to existing enums (if consumers handle unknown values gracefully)
- Widening type constraints (e.g., minLength 1→0)

**Breaking** (requires versioning/migration):
- Removing required fields
- Renaming fields
- Changing field types
- Tightening constraints (e.g., minLength 0→1)
- Changing event_type constant

**Versioning Strategy**:
```json
// Option 1: Create new event type for breaking changes
// Old: meeting.created
// New: meeting.created.v2

// Option 2: Add version field to payload
{
  "properties": {
    "schema_version": {
      "type": "integer",
      "const": 2,
      "description": "Schema version for breaking change detection"
    }
  }
}
```

#### 7. Pre-Commit Hook (Optional)

**File**: `.git/hooks/pre-commit` (in theboard repo)

```bash
#!/bin/bash
# Auto-regenerate Holyfields contracts if schemas changed

HOLYFIELDS_PATH="$HOME/code/33GOD/holyfields/trunk-main"

# Check if any Holyfields schemas changed
if git diff --cached --name-only | grep -q "holyfields.*\.json"; then
    echo "Holyfields schemas changed, regenerating contracts..."
    cd "$HOLYFIELDS_PATH"
    mise run generate:python || exit 1
    cd -
    echo "Contracts regenerated. Please review changes before committing."
fi
```

### Testing the Guide

Before finalizing, test the guide by:

1. **Fresh clone test**: Clone theboard repo fresh, follow guide steps → should work
2. **Error reproduction test**: Intentionally break things, follow troubleshooting → should fix
3. **New event test**: Add a fake new event following "Adding New Event Types" → should work
4. **Peer review**: Have another developer follow the guide without assistance

## Definition of Done

- [ ] Migration guide created with all sections
- [ ] Guide reviewed by at least 2 team members
- [ ] Guide tested with fresh repo clone
- [ ] All troubleshooting scenarios verified
- [ ] Example of adding new event tested end-to-end
- [ ] Guide linked from README.md
- [ ] Pre-commit hook template provided (optional)
- [ ] Guide committed to docs/ directory

## Related Documentation

Update these existing docs to reference the migration guide:

- `README.md` - Add "Event Contracts" section linking to guide
- `docs/events.md` - Add preamble explaining Holyfields contract system
- `docs/development.md` - Add "Working with Events" section
- `CONTRIBUTING.md` - Add "Event Schema Changes" workflow

## External Team Value

This guide serves as a template for other services adopting Holyfields:
- theboardroom (TypeScript consumer)
- Future Python services that emit theboard events
- Services that need to add their own event contracts

## Questions for Product Owner

1. Should we create a video walkthrough in addition to written guide?
2. Do we want to maintain a separate quick-reference cheat sheet?
3. Should the guide cover advanced topics (versioning, deprecation) or keep it simple?

## Success Metrics

- New developers can add an event type in <30 minutes
- Zero Holyfields-related support questions after 2 weeks
- All team members successfully adopt contracts without blocking issues

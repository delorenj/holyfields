# THEBOARD-002: Add Participant Turn Events

**Priority**: High
**Estimation**: 5 Story Points
**Team**: theboard
**Dependencies**: THEBOARD-001 (Adopt Holyfields Contracts)
**Blocked By**: THEBOARD-001

## User Story

As a theboardroom visualization developer, I want theboard to emit participant turn events (participant.added, participant.turn_started, participant.turn_completed) so that the 3D visualization can show real-time turn-by-turn updates instead of only round-level updates.

## Background

**Current State**: theboard emits 7 meeting-level events but NO participant-level turn events.

**Problem**: theboardroom visualization expects participant turn events to:
- Display participant avatars around the table (participant.added)
- Show who is currently speaking (participant.turn_started)
- Update speaking status when turn ends (participant.turn_completed)

**Impact**: Without these events, theboardroom can only show:
- ✅ Meeting-level state (created, started, completed)
- ✅ Round-level metrics (round_completed)
- ❌ Turn-by-turn speaking indicators (MISSING)
- ❌ Individual participant visualization (MISSING)

**Discovered By**: Integration readiness assessment between theboard and theboardroom (see `~/code/33GOD/theboardroom/trunk-main/docs/integration-readiness-assessment.md`)

## Acceptance Criteria

- [ ] Define 3 new event schemas in Holyfields repo:
  - `participant.added` - Emitted when agent is added to meeting participant list
  - `participant.turn_started` - Emitted when agent begins speaking in a round
  - `participant.turn_completed` - Emitted when agent finishes response in a round
- [ ] Implement event emission in theboard's MeetingOrchestrator:
  - Emit `participant.added` during meeting initialization for each selected agent
  - Emit `participant.turn_started` before calling agent's `respond()` method
  - Emit `participant.turn_completed` after agent response is processed
- [ ] Add unit tests for new event emissions
- [ ] Update theboard documentation to list all 10 emitted events
- [ ] Notify theboardroom team of new event availability

## Technical Implementation Notes

### Schema Definitions (Add to Holyfields)

Create in `~/code/33GOD/holyfields/trunk-main/theboard/events/`:

**participant_added.json**:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://33god.dev/schemas/theboard/events/participant_added.json",
  "title": "Participant Added Event",
  "description": "Emitted when agent is added to meeting participant list. Enables downstream visualizations to display avatars.",
  "type": "object",
  "allOf": [{"$ref": "../../common/schemas/base_event.json"}],
  "properties": {
    "event_type": {
      "type": "string",
      "const": "participant.added",
      "description": "Event type discriminator"
    },
    "agent_name": {
      "$ref": "../../common/schemas/types.json#/$defs/agent_name",
      "description": "Name of agent added as participant"
    },
    "position_index": {
      "type": "integer",
      "minimum": 0,
      "description": "Zero-based position in participant list (for spatial layout)"
    },
    "total_participants": {
      "type": "integer",
      "minimum": 1,
      "description": "Total number of participants in meeting"
    }
  },
  "required": ["event_type", "timestamp", "meeting_id", "agent_name", "position_index", "total_participants"],
  "additionalProperties": false
}
```

**participant_turn_started.json**:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://33god.dev/schemas/theboard/events/participant_turn_started.json",
  "title": "Participant Turn Started Event",
  "description": "Emitted when participant begins speaking in a round. Enables turn-by-turn speaking indicators.",
  "type": "object",
  "allOf": [{"$ref": "../../common/schemas/base_event.json"}],
  "properties": {
    "event_type": {
      "type": "string",
      "const": "participant.turn_started",
      "description": "Event type discriminator"
    },
    "round_num": {
      "$ref": "../../common/schemas/types.json#/$defs/round_number",
      "description": "Current round number"
    },
    "agent_name": {
      "$ref": "../../common/schemas/types.json#/$defs/agent_name",
      "description": "Name of agent starting turn"
    },
    "turn_type": {
      "type": "string",
      "enum": ["response", "turn"],
      "description": "Type of turn (response = replying to context, turn = initial contribution)"
    }
  },
  "required": ["event_type", "timestamp", "meeting_id", "round_num", "agent_name", "turn_type"],
  "additionalProperties": false
}
```

**participant_turn_completed.json**:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://33god.dev/schemas/theboard/events/participant_turn_completed.json",
  "title": "Participant Turn Completed Event",
  "description": "Emitted when participant finishes speaking in a round. Includes turn metrics.",
  "type": "object",
  "allOf": [{"$ref": "../../common/schemas/base_event.json"}],
  "properties": {
    "event_type": {
      "type": "string",
      "const": "participant.turn_completed",
      "description": "Event type discriminator"
    },
    "round_num": {
      "$ref": "../../common/schemas/types.json#/$defs/round_number",
      "description": "Current round number"
    },
    "agent_name": {
      "$ref": "../../common/schemas/types.json#/$defs/agent_name",
      "description": "Name of agent who completed turn"
    },
    "response_length": {
      "type": "integer",
      "minimum": 0,
      "description": "Character length of response"
    },
    "tokens_used": {
      "type": "integer",
      "minimum": 0,
      "description": "Tokens consumed in this turn"
    }
  },
  "required": ["event_type", "timestamp", "meeting_id", "round_num", "agent_name", "response_length", "tokens_used"],
  "additionalProperties": false
}
```

### Emission Points in theboard

**File**: `src/theboard/core/meeting.py` (MeetingOrchestrator class)

**Location 1: After agent selection** (emit participant.added):
```python
# In MeetingOrchestrator.start() method, after agent selection
for idx, agent in enumerate(self.selected_agents):
    self.event_emitter.emit(
        ParticipantAddedEvent(
            meeting_id=self.meeting_id,
            agent_name=agent.name,
            position_index=idx,
            total_participants=len(self.selected_agents)
        )
    )
```

**Location 2: Before agent response** (emit participant.turn_started):
```python
# In MeetingOrchestrator._run_round() method, before calling agent.respond()
self.event_emitter.emit(
    ParticipantTurnStartedEvent(
        meeting_id=self.meeting_id,
        round_num=self.current_round,
        agent_name=agent.name,
        turn_type="response" if self.current_round > 1 else "turn"
    )
)

# Then existing code:
response = agent.respond(prompt)
```

**Location 3: After agent response** (emit participant.turn_completed):
```python
# In MeetingOrchestrator._run_round() method, after processing response
self.event_emitter.emit(
    ParticipantTurnCompletedEvent(
        meeting_id=self.meeting_id,
        round_num=self.current_round,
        agent_name=agent.name,
        response_length=len(response.text),
        tokens_used=response.tokens_used
    )
)
```

### Testing Strategy

**Unit Tests** (`tests/events/test_participant_events.py`):
```python
def test_participant_added_emission():
    """Verify participant.added emitted for each agent during meeting start."""
    meeting = MeetingOrchestrator(topic="Test", agents=["Alice", "Bob", "Charlie"])

    with capture_events() as events:
        meeting.start()

    participant_events = [e for e in events if e.event_type == "participant.added"]
    assert len(participant_events) == 3
    assert participant_events[0].agent_name == "Alice"
    assert participant_events[0].position_index == 0
    assert participant_events[2].total_participants == 3

def test_turn_events_emission_order():
    """Verify turn_started emitted before turn_completed."""
    meeting = MeetingOrchestrator(topic="Test", agents=["Alice"])
    meeting.start()

    with capture_events() as events:
        meeting.run_round()

    turn_events = [e for e in events if "turn" in e.event_type]
    assert turn_events[0].event_type == "participant.turn_started"
    assert turn_events[-1].event_type == "participant.turn_completed"
    assert turn_events[0].agent_name == turn_events[-1].agent_name
```

**Integration Test**:
```python
def test_full_meeting_participant_event_flow():
    """Verify all participant events in realistic meeting scenario."""
    meeting = MeetingOrchestrator(
        topic="AI Safety",
        agents=["Alice", "Bob"],
        max_rounds=2
    )

    with capture_events() as events:
        meeting.start()
        meeting.run()

    # Should have: 2 participant.added + (2 turn_started + 2 turn_completed) * 2 rounds
    assert count_events(events, "participant.added") == 2
    assert count_events(events, "participant.turn_started") == 4  # 2 agents * 2 rounds
    assert count_events(events, "participant.turn_completed") == 4
```

## Event Sequence Example

For a 3-agent, 2-round meeting, events should be emitted in this order:

1. `meeting.created`
2. `meeting.started`
3. `participant.added` (Alice, pos=0)
4. `participant.added` (Bob, pos=1)
5. `participant.added` (Charlie, pos=2)
6. **Round 1:**
   - `participant.turn_started` (Alice)
   - `participant.turn_completed` (Alice)
   - `comment_extracted` (Alice's comments)
   - `participant.turn_started` (Bob)
   - `participant.turn_completed` (Bob)
   - `comment_extracted` (Bob's comments)
   - `participant.turn_started` (Charlie)
   - `participant.turn_completed` (Charlie)
   - `comment_extracted` (Charlie's comments)
   - `round_completed`
7. **Round 2:** (same pattern as Round 1)
8. `meeting.converged` (if convergence detected)
9. `meeting.completed`

## Impact on theboardroom

Once implemented, theboardroom can:
- ✅ Display participant avatars around the table (using participant.added)
- ✅ Highlight currently speaking participant (using participant.turn_started)
- ✅ Show turn-by-turn progression within rounds (using turn_completed)
- ✅ Display per-participant metrics (response length, token usage)

## Breaking Changes

**None**. These are new events that don't modify existing ones. Consumers that don't care about turn-level granularity can continue using only round-level events.

## Rollout Plan

1. **Phase 1**: Define schemas in Holyfields, regenerate contracts
2. **Phase 2**: Implement emissions in theboard, add tests
3. **Phase 3**: Update theboard documentation
4. **Phase 4**: Notify theboardroom team, update their event handlers
5. **Phase 5**: Update integration-readiness-assessment to show 10/10 events implemented

## Definition of Done

- [ ] All acceptance criteria met
- [ ] Unit tests for each event type passing
- [ ] Integration test for full event sequence passing
- [ ] Documentation updated (events.md, integration guide)
- [ ] Code review approved
- [ ] Changes merged to main branch
- [ ] theboardroom team notified via integration ticket

## Downstream Integration Ticket

Create in theboardroom repo:
- **THEBOARDROOM-TBD**: Consume participant turn events for real-time visualization

## Questions for Product Owner

1. Should `participant.added` events be emitted even if meeting fails during initialization?
2. Do we want to emit turn events during human-in-the-loop pauses (Sprint 4)?
3. Should we backfill these events for historical meetings in the database?

## External Team Coordination

**Downstream Consumer**: theboardroom
**Point of Contact**: @frontend-developer
**Notification Method**: Create integration ticket + Slack #bloodbank-events channel

**Consumer Readiness**: theboardroom already has event handlers waiting for these events (see `src/events/MockEventSource.ts` lines 45-65). They just need to be wired to real Bloodbank stream instead of mocks.

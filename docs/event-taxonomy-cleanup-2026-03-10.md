# Holyfields Event Taxonomy Cleanup (2026-03-10)

## Goal
Normalize event domains around stable business entities instead of implementation-specific namespaces.

## Canonical domains (v1 migration target)
- `agent.*`
- `artifact.*`
- `command.*`
- `session.*`
- `task.*`
- `meeting.*` (canonical replacement for `theboard.meeting.*`)
- `transcript.*` (canonical replacement for `fireflies.transcript.*`)
- `github.*`

## Newly added contracts
- `agent.memory.retained`
- `agent.memory.recalled`
- `artifact.image.detected`
- `artifact.video.detected`
- `artifact.document.detected`
- `meeting.{created,started,comment.extracted,converged,completed,failed,round.completed}`
- `transcript.{upload,ready,processed,failed}`

## Deprecation posture
- Keep `theboard.meeting.*` active as compatibility aliases for now.
- Keep `fireflies.transcript.*` active as compatibility aliases for now.
- Keep `llm.*` as deprecated (already marked in schema descriptions).
- Mark `asset.created` deprecated in favor of `artifact.*`.

## Memory event placement decision
Decision: memory hooks are under `agent.memory.*` with `session_key` in payload.

Rationale:
- Ownership remains agent-centric (memory bank and retention behavior belong to an agent).
- Session-level context is still first-class via `session_key`, enabling timeline and analytics by conversation instance.
- This avoids duplicating contracts across both `agent.*` and `session.*`.

## Next migration step (breaking change window)
1. Update producers to emit canonical `meeting.*` and `transcript.*` types.
2. Update consumers to subscribe to canonical types first, aliases second.
3. Remove legacy aliases in `theboard.*` and `fireflies.*` after verified cutover.

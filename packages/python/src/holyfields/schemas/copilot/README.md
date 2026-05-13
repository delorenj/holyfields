# copilot.* schemas

CloudEvents 1.0 envelopes for GitHub Copilot CLI hook events, published by
`bloodbank/services/agent-hooks/copilot/publish.py`.

Reference: <https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-hooks>

## Pattern

Each schema:

- Inherits the envelope shape from `_common/cloudevent_base.v1.json` via `allOf`.
- Locks the envelope `type` and `domain` to the event's identity.
- Constrains the `data` block to `{hook: <const>, payload: object}`. The
  `payload` is a passthrough of the Copilot-supplied hook JSON and is treated
  as opaque — each Copilot release may add fields without breaking consumers.

## Event types

| File | type | NATS subject | Copilot hook |
|---|---|---|---|
| `session.started.v1.json`  | `copilot.session.started`  | `event.copilot.session.started`  | `sessionStart`        |
| `session.ended.v1.json`    | `copilot.session.ended`    | `event.copilot.session.ended`    | `sessionEnd`          |
| `prompt.submitted.v1.json` | `copilot.prompt.submitted` | `event.copilot.prompt.submitted` | `userPromptSubmitted` |
| `tool.pre.v1.json`         | `copilot.tool.pre`         | `event.copilot.tool.pre`         | `preToolUse`          |
| `tool.post.v1.json`        | `copilot.tool.post`        | `event.copilot.tool.post`        | `postToolUse`         |
| `error.occurred.v1.json`   | `copilot.error.occurred`   | `event.copilot.error.occurred`   | `errorOccurred`       |
| `agent.stopped.v1.json`    | `copilot.agent.stopped`    | `event.copilot.agent.stopped`    | `agentStop`           |

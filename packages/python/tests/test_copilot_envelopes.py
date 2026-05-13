"""Round-trip validation for all 7 copilot.* event schemas.

Each copilot.* event has the same envelope shape (cloudevent_base) and a
``data`` block locked to ``{hook: <const>, payload: object}``. This file
parametrizes over every type so adding an 8th copilot event needs one new
row, not a new file.

Producer reference: bloodbank/services/agent-hooks/copilot/publish.py.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import jsonschema
import pytest
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

SCHEMAS_DIR = Path(__file__).resolve().parents[3] / "schemas"
COPILOT_DIR = SCHEMAS_DIR / "copilot"
BASE_SCHEMA_PATH = SCHEMAS_DIR / "_common" / "cloudevent_base.v1.json"
TYPES_SCHEMA_PATH = SCHEMAS_DIR / "_common" / "types.v1.json"

# (filename-stem, ce_type, hook-name)
COPILOT_EVENTS = [
    ("session.started",  "copilot.session.started",  "sessionStart"),
    ("session.ended",    "copilot.session.ended",    "sessionEnd"),
    ("prompt.submitted", "copilot.prompt.submitted", "userPromptSubmitted"),
    ("tool.pre",         "copilot.tool.pre",         "preToolUse"),
    ("tool.post",        "copilot.tool.post",        "postToolUse"),
    ("error.occurred",   "copilot.error.occurred",   "errorOccurred"),
    ("agent.stopped",    "copilot.agent.stopped",    "agentStop"),
]


def _registry(base: dict, types: dict) -> Registry:
    return (
        Registry()
        .with_resource(
            uri="https://33god.dev/schemas/_common/cloudevent_base.v1.json",
            resource=Resource.from_contents(base, default_specification=DRAFT202012),
        )
        .with_resource(
            uri="../_common/cloudevent_base.v1.json",
            resource=Resource.from_contents(base, default_specification=DRAFT202012),
        )
        .with_resource(
            uri="https://33god.dev/schemas/_common/types.v1.json",
            resource=Resource.from_contents(types, default_specification=DRAFT202012),
        )
        .with_resource(
            uri="types.v1.json",
            resource=Resource.from_contents(types, default_specification=DRAFT202012),
        )
        .with_resource(
            uri="../_common/types.v1.json",
            resource=Resource.from_contents(types, default_specification=DRAFT202012),
        )
    )


def _validator_for(stem: str) -> jsonschema.protocols.Validator:
    schema_path = COPILOT_DIR / f"{stem}.v1.json"
    schema = json.loads(schema_path.read_text())
    base = json.loads(BASE_SCHEMA_PATH.read_text())
    types = json.loads(TYPES_SCHEMA_PATH.read_text())
    return jsonschema.Draft202012Validator(
        schema,
        registry=_registry(base, types),
        format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
    )


def _canonical(*, ce_type: str, hook: str, **overrides: object) -> dict:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    session_id = str(uuid.uuid4())
    base = {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "source": "urn:33god:integration:copilot-cli",
        "type": ce_type,
        "subject": f"copilot/{hook}",
        "time": now,
        "datacontenttype": "application/json",
        "correlationid": session_id,
        "causationid": session_id,
        "producer": "copilot-cli",
        "service": "copilot-hooks",
        "domain": "copilot",
        "schemaref": f"{ce_type}.v1",
        "traceparent": "00-00000000000000000000000000000000-0000000000000000-00",
        "data": {
            "hook": hook,
            "payload": {"probe": True},
        },
    }
    base.update(overrides)
    return base


@pytest.mark.parametrize("stem, ce_type, hook", COPILOT_EVENTS)
class TestCopilotEnvelope:
    def test_canonical_envelope_validates(self, stem, ce_type, hook):
        validator = _validator_for(stem)
        env = _canonical(ce_type=ce_type, hook=hook)
        errors = sorted(validator.iter_errors(env), key=lambda e: list(e.path))
        assert not errors, f"{stem}: {[e.message for e in errors]}"

    def test_type_locked_to_constant(self, stem, ce_type, hook):
        validator = _validator_for(stem)
        env = _canonical(ce_type=ce_type, hook=hook, type="copilot.bogus.event")
        assert list(validator.iter_errors(env)), f"{stem}: type must be locked"

    def test_domain_locked_to_copilot(self, stem, ce_type, hook):
        validator = _validator_for(stem)
        env = _canonical(ce_type=ce_type, hook=hook, domain="agent")
        assert list(validator.iter_errors(env)), f"{stem}: domain must be 'copilot'"

    def test_hook_locked_to_constant(self, stem, ce_type, hook):
        validator = _validator_for(stem)
        env = _canonical(ce_type=ce_type, hook=hook)
        env["data"]["hook"] = "somethingElse"
        assert list(validator.iter_errors(env)), f"{stem}: hook must be locked to {hook!r}"

    def test_payload_required(self, stem, ce_type, hook):
        validator = _validator_for(stem)
        env = _canonical(ce_type=ce_type, hook=hook)
        del env["data"]["payload"]
        assert list(validator.iter_errors(env)), f"{stem}: payload is required"

    def test_no_extra_data_fields(self, stem, ce_type, hook):
        validator = _validator_for(stem)
        env = _canonical(ce_type=ce_type, hook=hook)
        env["data"]["surprise"] = "value"
        assert list(validator.iter_errors(env)), f"{stem}: additionalProperties=false"

    def test_correlationid_uuid_format_inherited(self, stem, ce_type, hook):
        validator = _validator_for(stem)
        env = _canonical(ce_type=ce_type, hook=hook, correlationid="not-a-uuid")
        assert list(validator.iter_errors(env)), f"{stem}: correlationid must be a uuid"

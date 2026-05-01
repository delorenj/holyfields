"""Round-trip validation for agent.prompt.submitted.v1 (v3 base)."""

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
SCHEMA_PATH = SCHEMAS_DIR / "agent" / "prompt.submitted.v1.json"
BASE_SCHEMA_PATH = SCHEMAS_DIR / "_common" / "cloudevent_base.v1.json"
TYPES_SCHEMA_PATH = SCHEMAS_DIR / "_common" / "types.v1.json"


def _load_validator() -> jsonschema.protocols.Validator:
    schema = json.loads(SCHEMA_PATH.read_text())
    base = json.loads(BASE_SCHEMA_PATH.read_text())
    types = json.loads(TYPES_SCHEMA_PATH.read_text())

    registry = (
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
    return jsonschema.Draft202012Validator(
        schema,
        registry=registry,
        format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
    )


@pytest.fixture(scope="module")
def validator() -> jsonschema.protocols.Validator:
    return _load_validator()


def _canonical(**overrides: object) -> dict:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    sid = str(uuid.uuid4())
    base = {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "source": "urn:33god:agent:claude-code",
        "type": "agent.prompt.submitted",
        "subject": f"agent/{sid}",
        "time": now,
        "datacontenttype": "application/json",
        "correlationid": sid,
        "causationid": None,
        "producer": "claude-code",
        "service": "claude-code",
        "domain": "agent",
        "schemaref": "agent.prompt.submitted.v1",
        "traceparent": "00-00000000000000000000000000000000-0000000000000000-00",
        "data": {
            "session_id": sid,
            "prompt_text": "list the files in .claude/hooks",
            "prompt_length": 32,
            "working_directory": "/home/jarad/code/33GOD",
            "git_branch": "main",
        },
    }
    base.update(overrides)
    return base


class TestAgentPromptSubmittedV1:
    def test_canonical_envelope_validates(self, validator) -> None:
        env = _canonical()
        errors = sorted(validator.iter_errors(env), key=lambda e: list(e.path))
        assert not errors, f"canonical envelope failed: {[e.message for e in errors]}"

    def test_type_locked_to_constant(self, validator) -> None:
        env = _canonical(type="agent.prompt.received")
        assert list(validator.iter_errors(env)), "type must be locked"

    def test_domain_locked_to_constant(self, validator) -> None:
        env = _canonical(domain="system")
        assert list(validator.iter_errors(env)), "domain must be locked to 'agent'"

    def test_session_id_required_and_uuid(self, validator) -> None:
        env = _canonical()
        del env["data"]["session_id"]
        assert list(validator.iter_errors(env)), "session_id required"

        env = _canonical()
        env["data"]["session_id"] = "not-uuid"
        assert list(validator.iter_errors(env)), "session_id must be uuid"

    def test_prompt_text_required(self, validator) -> None:
        env = _canonical()
        del env["data"]["prompt_text"]
        assert list(validator.iter_errors(env)), "prompt_text is required"

    def test_prompt_length_required_non_negative(self, validator) -> None:
        env = _canonical()
        del env["data"]["prompt_length"]
        assert list(validator.iter_errors(env)), "prompt_length is required"

        env = _canonical()
        env["data"]["prompt_length"] = -1
        assert list(validator.iter_errors(env)), "prompt_length must be >= 0"

    def test_empty_prompt_text_allowed(self, validator) -> None:
        # Empty prompt is unusual but legal; validation enforces presence not content.
        env = _canonical()
        env["data"]["prompt_text"] = ""
        env["data"]["prompt_length"] = 0
        assert not list(validator.iter_errors(env)), "empty prompt should validate"

    def test_working_directory_optional(self, validator) -> None:
        env = _canonical()
        del env["data"]["working_directory"]
        assert not list(validator.iter_errors(env)), "working_directory is optional"

    def test_git_branch_optional(self, validator) -> None:
        env = _canonical()
        del env["data"]["git_branch"]
        assert not list(validator.iter_errors(env)), "git_branch is optional"

    def test_no_extra_data_fields(self, validator) -> None:
        env = _canonical()
        env["data"]["sneaky_extra"] = "bad"
        assert list(validator.iter_errors(env)), "additionalProperties: false should reject extras"

    def test_inherits_cloudevent_base_requirements(self, validator) -> None:
        for field in ("specversion", "id", "source", "time", "correlationid", "producer", "service"):
            env = _canonical()
            del env[field]
            assert list(validator.iter_errors(env)), f"missing inherited base field {field!r} should fail"

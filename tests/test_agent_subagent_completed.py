"""Round-trip validation for agent.subagent.completed.v1 (v3 base)."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import jsonschema
import pytest
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"
SCHEMA_PATH = SCHEMAS_DIR / "agent" / "subagent.completed.v1.json"
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
    parent_session = str(uuid.uuid4())
    base = {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "source": "urn:33god:agent:claude-code",
        "type": "agent.subagent.completed",
        "subject": f"agent/{parent_session}/subagent",
        "time": now,
        "datacontenttype": "application/json",
        "correlationid": parent_session,
        "causationid": None,
        "producer": "claude-code",
        "service": "claude-code",
        "domain": "agent",
        "schemaref": "agent.subagent.completed.v1",
        "traceparent": "00-00000000000000000000000000000000-0000000000000000-00",
        "data": {
            "session_id": parent_session,
            "agent_type": "general-purpose",
            "stop_reason": "completed",
            "working_directory": "/home/jarad/code/33GOD",
        },
    }
    base.update(overrides)
    return base


class TestAgentSubagentCompletedV1:
    def test_canonical_envelope_validates(self, validator) -> None:
        env = _canonical()
        errors = sorted(validator.iter_errors(env), key=lambda e: list(e.path))
        assert not errors, f"canonical envelope failed: {[e.message for e in errors]}"

    def test_type_locked_to_constant(self, validator) -> None:
        env = _canonical(type="agent.subagent.spawned")
        assert list(validator.iter_errors(env)), "type must be locked"

    def test_domain_locked_to_constant(self, validator) -> None:
        env = _canonical(domain="system")
        assert list(validator.iter_errors(env)), "domain must be locked to 'agent'"

    def test_session_id_required_and_uuid(self, validator) -> None:
        env = _canonical()
        del env["data"]["session_id"]
        assert list(validator.iter_errors(env)), "session_id required"

        env = _canonical()
        env["data"]["session_id"] = "nope"
        assert list(validator.iter_errors(env)), "session_id must be uuid"

    def test_stop_reason_required_enum(self, validator) -> None:
        env = _canonical()
        del env["data"]["stop_reason"]
        assert list(validator.iter_errors(env)), "stop_reason is required"

        env = _canonical()
        env["data"]["stop_reason"] = "exploded"
        assert list(validator.iter_errors(env)), "stop_reason restricted to enum"

        for v in ["completed", "error", "timeout", "user_stop"]:
            env = _canonical()
            env["data"]["stop_reason"] = v
            assert not list(validator.iter_errors(env)), f"{v} should be valid"

    def test_agent_type_optional(self, validator) -> None:
        env = _canonical()
        del env["data"]["agent_type"]
        assert not list(validator.iter_errors(env)), "agent_type is optional"

    def test_working_directory_optional(self, validator) -> None:
        env = _canonical()
        del env["data"]["working_directory"]
        assert not list(validator.iter_errors(env)), "working_directory is optional"

    def test_no_extra_data_fields(self, validator) -> None:
        env = _canonical()
        env["data"]["sneaky_extra"] = "bad"
        assert list(validator.iter_errors(env)), "additionalProperties: false should reject extras"

    def test_inherits_cloudevent_base_requirements(self, validator) -> None:
        for field in ("specversion", "id", "source", "time", "correlationid", "producer", "service"):
            env = _canonical()
            del env[field]
            assert list(validator.iter_errors(env)), f"missing inherited base field {field!r} should fail"

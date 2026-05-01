"""Round-trip validation for agent.session.ended.v1 (v3 base)."""

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
SCHEMA_PATH = SCHEMAS_DIR / "agent" / "session.ended.v1.json"
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
    session_id = str(uuid.uuid4())
    base = {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "source": "urn:33god:agent:claude-code",
        "type": "agent.session.ended",
        "subject": f"agent/{session_id}",
        "time": now,
        "datacontenttype": "application/json",
        "correlationid": session_id,
        "causationid": None,
        "producer": "claude-code",
        "service": "claude-code",
        "domain": "agent",
        "schemaref": "agent.session.ended.v1",
        "traceparent": "00-00000000000000000000000000000000-0000000000000000-00",
        "data": {
            "session_id": session_id,
            "end_reason": "user_stop",
            "duration_seconds": 1234,
            "total_turns": 17,
            "tools_used": {"Bash": 8, "Read": 5, "Edit": 4},
            "files_modified": ["src/app.py", "tests/test_app.py"],
            "git_commits": ["a1b2c3d4e5f6", "deadbeef1234"],
            "final_status": "success",
            "working_directory": "/home/jarad/code/33GOD",
            "git_branch": "main",
        },
    }
    base.update(overrides)
    return base


class TestAgentSessionEndedV1:
    def test_canonical_envelope_validates(self, validator) -> None:
        env = _canonical()
        errors = sorted(validator.iter_errors(env), key=lambda e: list(e.path))
        assert not errors, f"canonical envelope failed: {[e.message for e in errors]}"

    def test_type_locked_to_constant(self, validator) -> None:
        env = _canonical(type="agent.session.aborted")
        assert list(validator.iter_errors(env)), "type must be locked to 'agent.session.ended'"

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

    def test_end_reason_enum(self, validator) -> None:
        env = _canonical()
        env["data"]["end_reason"] = "spontaneous"
        assert list(validator.iter_errors(env)), "end_reason restricted to enum"
        for v in ["user_stop", "completed", "error", "timeout", "context_full"]:
            env = _canonical()
            env["data"]["end_reason"] = v
            assert not list(validator.iter_errors(env)), f"{v} should be a valid end_reason"

    def test_duration_seconds_required_non_negative(self, validator) -> None:
        env = _canonical()
        del env["data"]["duration_seconds"]
        assert list(validator.iter_errors(env)), "duration_seconds is required"

        env = _canonical()
        env["data"]["duration_seconds"] = -1
        assert list(validator.iter_errors(env)), "duration_seconds must be >= 0"

    def test_total_turns_required_non_negative(self, validator) -> None:
        env = _canonical()
        del env["data"]["total_turns"]
        assert list(validator.iter_errors(env)), "total_turns is required"

        env = _canonical()
        env["data"]["total_turns"] = -1
        assert list(validator.iter_errors(env)), "total_turns must be >= 0"

    def test_tools_used_optional_but_constrained(self, validator) -> None:
        env = _canonical()
        del env["data"]["tools_used"]
        assert not list(validator.iter_errors(env)), "tools_used is optional"

        env = _canonical()
        env["data"]["tools_used"] = {"Bash": -1}
        assert list(validator.iter_errors(env)), "tools_used counts must be >= 0"

    def test_final_status_enum(self, validator) -> None:
        env = _canonical()
        env["data"]["final_status"] = "almost"
        assert list(validator.iter_errors(env)), "final_status restricted to enum"

    def test_no_extra_data_fields(self, validator) -> None:
        env = _canonical()
        env["data"]["sneaky_extra"] = "bad"
        assert list(validator.iter_errors(env)), "additionalProperties: false should reject extras"

    def test_inherits_cloudevent_base_requirements(self, validator) -> None:
        for field in ("specversion", "id", "source", "time", "correlationid", "producer", "service"):
            env = _canonical()
            del env[field]
            assert list(validator.iter_errors(env)), f"missing inherited base field {field!r} should fail"

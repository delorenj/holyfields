"""Round-trip validation for agent.tool.invoked.v1 (v3 base)."""

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
SCHEMA_PATH = SCHEMAS_DIR / "agent" / "tool.invoked.v1.json"
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
        "type": "agent.tool.invoked",
        "subject": f"agent/{session_id}/tool/Bash",
        "time": now,
        "datacontenttype": "application/json",
        "correlationid": session_id,
        "causationid": None,
        "producer": "claude-code",
        "service": "claude-code",
        "domain": "agent",
        "schemaref": "agent.tool.invoked.v1",
        "traceparent": "00-00000000000000000000000000000000-0000000000000000-00",
        "data": {
            "session_id": session_id,
            "tool_name": "Bash",
            "tool_input": {"command": "ls -la", "description": "list directory"},
            "working_directory": "/home/jarad/code/33GOD",
            "git_branch": "main",
            "git_status": "clean",
            "turn_number": 3,
            "success": True,
        },
    }
    base.update(overrides)
    return base


class TestAgentToolInvokedV1:
    def test_canonical_envelope_validates(self, validator) -> None:
        env = _canonical()
        errors = sorted(validator.iter_errors(env), key=lambda e: list(e.path))
        assert not errors, f"canonical envelope failed: {[e.message for e in errors]}"

    def test_type_locked_to_constant(self, validator) -> None:
        env = _canonical(type="agent.tool.completed")
        assert list(validator.iter_errors(env)), "type must be locked to 'agent.tool.invoked'"

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

    def test_tool_name_required_min_length(self, validator) -> None:
        env = _canonical()
        del env["data"]["tool_name"]
        assert list(validator.iter_errors(env)), "tool_name is required"

        env = _canonical()
        env["data"]["tool_name"] = ""
        assert list(validator.iter_errors(env)), "tool_name min length 1"

    def test_turn_number_required_positive(self, validator) -> None:
        env = _canonical()
        del env["data"]["turn_number"]
        assert list(validator.iter_errors(env)), "turn_number is required"

        env = _canonical()
        env["data"]["turn_number"] = 0
        assert list(validator.iter_errors(env)), "turn_number must be >= 1"

    def test_tool_input_arbitrary_object(self, validator) -> None:
        # tool_input is intentionally unconstrained beyond type=object.
        for shape in [
            {},
            {"a": 1},
            {"command": "x", "nested": {"deep": [1, 2, 3]}},
        ]:
            env = _canonical()
            env["data"]["tool_input"] = shape
            assert not list(validator.iter_errors(env)), f"tool_input should accept {shape}"

    def test_tool_input_optional(self, validator) -> None:
        env = _canonical()
        del env["data"]["tool_input"]
        assert not list(validator.iter_errors(env)), "tool_input is optional"

    def test_git_status_enum(self, validator) -> None:
        env = _canonical()
        env["data"]["git_status"] = "dirty"
        assert list(validator.iter_errors(env)), "git_status restricted to enum"
        for v in ["clean", "modified"]:
            env = _canonical()
            env["data"]["git_status"] = v
            assert not list(validator.iter_errors(env)), f"{v} valid"

    def test_no_extra_data_fields(self, validator) -> None:
        env = _canonical()
        env["data"]["sneaky_extra"] = "bad"
        assert list(validator.iter_errors(env)), "additionalProperties: false should reject extras"

    def test_inherits_cloudevent_base_requirements(self, validator) -> None:
        for field in ("specversion", "id", "source", "time", "correlationid", "producer", "service"):
            env = _canonical()
            del env[field]
            assert list(validator.iter_errors(env)), f"missing inherited base field {field!r} should fail"

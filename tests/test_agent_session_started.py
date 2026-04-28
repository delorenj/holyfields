"""Round-trip validation for agent.session.started.v1 (v3 base).

Mirrors test_heartbeat_tick.py: builds canonical envelopes, validates
them against the schema, and exercises the lock/required-field
contracts. The schema extends `_common/cloudevent_base.v1.json` via
`allOf`, so the inherited CloudEvents fields are also exercised.

Producer reference: 33GOD metarepo `.claude/hooks/bloodbank-publisher.sh`.
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

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"
SCHEMA_PATH = SCHEMAS_DIR / "agent" / "session.started.v1.json"
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
    """Build a minimally complete agent.session.started.v1 envelope."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    session_id = str(uuid.uuid4())
    base = {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "source": "urn:33god:agent:claude-code",
        "type": "agent.session.started",
        "subject": f"agent/{session_id}",
        "time": now,
        "datacontenttype": "application/json",
        "correlationid": session_id,
        "causationid": None,
        "producer": "claude-code",
        "service": "claude-code",
        "domain": "agent",
        "schemaref": "agent.session.started.v1",
        "traceparent": "00-00000000000000000000000000000000-0000000000000000-00",
        "data": {
            "session_id": session_id,
            "working_directory": "/home/jarad/code/33GOD",
            "git_branch": "main",
            "git_remote": "git@github.com:delorenj/33GOD.git",
            "started_at": now,
        },
    }
    base.update(overrides)
    return base


class TestAgentSessionStartedV1:
    def test_canonical_envelope_validates(self, validator) -> None:
        env = _canonical()
        errors = sorted(validator.iter_errors(env), key=lambda e: list(e.path))
        assert not errors, f"canonical envelope failed: {[e.message for e in errors]}"

    def test_type_locked_to_constant(self, validator) -> None:
        env = _canonical(type="agent.session.resumed")
        assert list(validator.iter_errors(env)), "type must be locked to 'agent.session.started'"

    def test_domain_locked_to_constant(self, validator) -> None:
        env = _canonical(domain="system")
        assert list(validator.iter_errors(env)), "domain must be locked to 'agent'"

    def test_session_id_required(self, validator) -> None:
        env = _canonical()
        del env["data"]["session_id"]
        assert list(validator.iter_errors(env)), "session_id is required"

    def test_session_id_must_be_uuid(self, validator) -> None:
        env = _canonical()
        env["data"]["session_id"] = "not-a-uuid"
        assert list(validator.iter_errors(env)), "session_id must be a uuid"

    def test_working_directory_required(self, validator) -> None:
        env = _canonical()
        del env["data"]["working_directory"]
        assert list(validator.iter_errors(env)), "working_directory is required"

    def test_started_at_required(self, validator) -> None:
        env = _canonical()
        del env["data"]["started_at"]
        assert list(validator.iter_errors(env)), "started_at is required"

    def test_git_remote_optional(self, validator) -> None:
        env = _canonical()
        del env["data"]["git_remote"]
        assert not list(validator.iter_errors(env)), "git_remote is optional"

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

    def test_correlationid_uuid_format_inherited(self, validator) -> None:
        env = _canonical(correlationid="not-a-uuid")
        assert list(validator.iter_errors(env)), "correlationid uuid format inherited from base"

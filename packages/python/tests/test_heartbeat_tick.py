"""Round-trip validation for system.heartbeat.tick.v1 — first real-world v3 event.

Mirrors the structure of test_cloudevent_base.py: builds canonical
envelopes, validates them against the schema, and checks failure cases.
The schema extends `_common/cloudevent_base.v1.json` via `allOf`, so we
exercise both the inherited CloudEvents fields and the heartbeat-specific
`data` payload.

See:
- `schemas/system/heartbeat.tick.v1.json`
- `33GOD/docs/architecture/holyfields-cloudevents-audit-2026-04-24.md`
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
TICK_SCHEMA_PATH = SCHEMAS_DIR / "system" / "heartbeat.tick.v1.json"
BASE_SCHEMA_PATH = SCHEMAS_DIR / "_common" / "cloudevent_base.v1.json"
TYPES_SCHEMA_PATH = SCHEMAS_DIR / "_common" / "types.v1.json"


def _load_validator() -> jsonschema.protocols.Validator:
    """Build a validator for heartbeat.tick.v1 with $refs resolved locally.

    Schema graph: heartbeat.tick.v1 -> cloudevent_base.v1 -> types.v1.
    All three load into a single registry so the validator can chase
    every $ref without network access.
    """
    tick = json.loads(TICK_SCHEMA_PATH.read_text())
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
        tick,
        registry=registry,
        format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
    )


@pytest.fixture(scope="module")
def validator() -> jsonschema.protocols.Validator:
    return _load_validator()


def _canonical_tick(**overrides: object) -> dict:
    """Build a minimally complete heartbeat.tick.v1 envelope."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    started_at = now
    base = {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "source": "urn:33god:service:heartbeat-tick",
        "type": "system.heartbeat.tick",
        "subject": "system/heartbeat-tick:test-1",
        "time": now,
        "datacontenttype": "application/json",
        "dataschema": "apicurio://holyfields/system.heartbeat.tick/versions/1",
        "correlationid": str(uuid.uuid4()),
        "causationid": None,
        "producer": "heartbeat-tick",
        "service": "heartbeat-tick",
        "domain": "system",
        "schemaref": "system.heartbeat.tick.v1",
        "traceparent": "00-00000000000000000000000000000000-0000000000000000-00",
        "data": {
            "tick_seq": 0,
            "interval_ms": 10000,
            "producer_id": "heartbeat-tick:test-1",
            "started_at": started_at,
        },
    }
    base.update(overrides)
    return base


class TestHeartbeatTickV1:
    def test_canonical_envelope_validates(self, validator) -> None:
        env = _canonical_tick()
        errors = sorted(validator.iter_errors(env), key=lambda e: list(e.path))
        assert not errors, f"canonical heartbeat failed: {[e.message for e in errors]}"

    def test_type_locked_to_constant(self, validator) -> None:
        env = _canonical_tick(type="system.heartbeat.pulse")
        errors = list(validator.iter_errors(env))
        assert errors, "type must be locked to 'system.heartbeat.tick'"

    def test_domain_locked_to_constant(self, validator) -> None:
        env = _canonical_tick(domain="agent")
        errors = list(validator.iter_errors(env))
        assert errors, "domain must be locked to 'system'"

    def test_tick_seq_required(self, validator) -> None:
        env = _canonical_tick()
        del env["data"]["tick_seq"]
        errors = list(validator.iter_errors(env))
        assert errors, "tick_seq is required"

    def test_tick_seq_must_be_non_negative(self, validator) -> None:
        env = _canonical_tick()
        env["data"]["tick_seq"] = -1
        errors = list(validator.iter_errors(env))
        assert errors, "tick_seq must be >= 0"

    def test_producer_id_required(self, validator) -> None:
        env = _canonical_tick()
        del env["data"]["producer_id"]
        errors = list(validator.iter_errors(env))
        assert errors, "producer_id is required"

    def test_started_at_required(self, validator) -> None:
        env = _canonical_tick()
        del env["data"]["started_at"]
        errors = list(validator.iter_errors(env))
        assert errors, "started_at is required"

    def test_interval_ms_optional_but_constrained(self, validator) -> None:
        env = _canonical_tick()
        del env["data"]["interval_ms"]
        assert not list(validator.iter_errors(env)), "interval_ms is optional"

        env = _canonical_tick()
        env["data"]["interval_ms"] = 50
        errors = list(validator.iter_errors(env))
        assert errors, "interval_ms must be >= 100"

    def test_no_extra_data_fields(self, validator) -> None:
        env = _canonical_tick()
        env["data"]["sneaky_extra"] = "bad"
        errors = list(validator.iter_errors(env))
        assert errors, "additionalProperties: false on data should reject extras"

    def test_inherits_cloudevent_base_requirements(self, validator) -> None:
        """The allOf $ref to cloudevent_base means base required fields apply too."""
        for field in ("specversion", "id", "source", "time", "correlationid", "producer", "service"):
            env = _canonical_tick()
            del env[field]
            errors = list(validator.iter_errors(env))
            assert errors, f"missing inherited base field {field!r} should fail"

    def test_specversion_inherited_constraint(self, validator) -> None:
        env = _canonical_tick(specversion="0.3")
        errors = list(validator.iter_errors(env))
        assert errors, "specversion != '1.0' inherited from base should still fail"

    def test_correlationid_uuid_format_inherited(self, validator) -> None:
        env = _canonical_tick(correlationid="not-a-uuid")
        errors = list(validator.iter_errors(env))
        assert errors, "correlationid uuid format inherited from base"

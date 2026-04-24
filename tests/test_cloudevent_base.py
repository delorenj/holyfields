"""Round-trip validation for the v3 CloudEvents base envelope.

This test constructs a canonical envelope in the exact shape Dapr accepts
(and has been proven to preserve in the bloodbank smoke tests), then
validates it against `_common/cloudevent_base.v1.json`. If this test ever
fails after a schema edit, the schema has drifted from the wire contract.

See:
- `../../docs/architecture/holyfields-cloudevents-audit-2026-04-24.md` (metarepo)
- `bloodbank/ops/v3/smoketest/smoketest-dapr.sh` (live proof of the shape)
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import jsonschema
import pytest

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"
BASE_SCHEMA_PATH = SCHEMAS_DIR / "_common" / "cloudevent_base.v1.json"
TYPES_SCHEMA_PATH = SCHEMAS_DIR / "_common" / "types.v1.json"


def _load_validator() -> jsonschema.protocols.Validator:
    """Build a jsonschema validator with local $ref resolution for types.v1.json."""
    base = json.loads(BASE_SCHEMA_PATH.read_text())
    types = json.loads(TYPES_SCHEMA_PATH.read_text())

    # Use a Registry so $ref to types.v1.json resolves against our local file.
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012

    registry = (
        Resource.from_contents(types, default_specification=DRAFT202012).lookup("").add_to(Registry())
        if False  # noqa: E501 placeholder for alt shape, unused
        else Registry().with_resource(
            uri="https://33god.dev/schemas/_common/types.v1.json",
            resource=Resource.from_contents(types, default_specification=DRAFT202012),
        ).with_resource(
            uri="types.v1.json",
            resource=Resource.from_contents(types, default_specification=DRAFT202012),
        )
    )

    # Enforce `format: uuid` etc. — jsonschema ignores format by default, which
    # would silently accept strings like "not-a-uuid" as valid UUIDs.
    return jsonschema.Draft202012Validator(
        base,
        registry=registry,
        format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
    )


@pytest.fixture(scope="module")
def validator() -> jsonschema.protocols.Validator:
    return _load_validator()


def _canonical_envelope(**overrides: object) -> dict:
    """Build a minimally complete v3 CloudEvents envelope for tests."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    base = {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "source": "urn:33god:service:holyfields-test",
        "type": "holyfields.test.emit",
        "subject": "holyfields-test/round-trip",
        "time": now,
        "datacontenttype": "application/json",
        "dataschema": "apicurio://holyfields/holyfields.test.emit/versions/1",
        "correlationid": str(uuid.uuid4()),
        "causationid": None,
        "producer": "holyfields-test",
        "service": "holyfields-test",
        "domain": "holyfields-test",
        "schemaref": "holyfields.test.emit.v1",
        "traceparent": "00-00000000000000000000000000000000-0000000000000000-00",
        "data": {"ok": True},
    }
    base.update(overrides)
    return base


class TestCloudEventBaseV1:
    def test_canonical_envelope_validates(self, validator) -> None:
        envelope = _canonical_envelope()
        errors = sorted(validator.iter_errors(envelope), key=lambda e: e.path)
        assert not errors, f"canonical envelope failed validation: {[e.message for e in errors]}"

    def test_missing_specversion_fails(self, validator) -> None:
        env = _canonical_envelope()
        del env["specversion"]
        assert list(validator.iter_errors(env)), "missing specversion should fail"

    def test_wrong_specversion_fails(self, validator) -> None:
        env = _canonical_envelope(specversion="0.3")
        assert list(validator.iter_errors(env)), "specversion != '1.0' should fail"

    def test_source_must_be_string(self, validator) -> None:
        env = _canonical_envelope(source={"host": "h", "app": "a", "trigger_type": "cli"})
        assert list(validator.iter_errors(env)), "object-shaped source should fail (CloudEvents requires URI string)"

    def test_type_pattern_enforced(self, validator) -> None:
        env = _canonical_envelope(type="Weather.Reading")
        assert list(validator.iter_errors(env)), "capital letters / uppercase should fail type pattern"
        env = _canonical_envelope(type="weather")
        assert list(validator.iter_errors(env)), "undotted type should fail pattern"

    def test_correlationid_must_be_uuid(self, validator) -> None:
        env = _canonical_envelope(correlationid="not-a-uuid")
        assert list(validator.iter_errors(env)), "non-UUID correlationid should fail"

    def test_causationid_nullable(self, validator) -> None:
        env = _canonical_envelope(causationid=None)
        assert not list(validator.iter_errors(env)), "null causationid should pass"
        env = _canonical_envelope(causationid=str(uuid.uuid4()))
        assert not list(validator.iter_errors(env)), "uuid causationid should pass"

    def test_traceparent_pattern(self, validator) -> None:
        env = _canonical_envelope(traceparent="bad")
        assert list(validator.iter_errors(env)), "bad traceparent should fail"
        env = _canonical_envelope(traceparent="00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01")
        assert not list(validator.iter_errors(env)), "real traceparent should pass"

    def test_all_33god_extension_fields_required(self, validator) -> None:
        """correlationid, producer, service, domain are required per ADR-0001."""
        for field in ("correlationid", "producer", "service", "domain"):
            env = _canonical_envelope()
            del env[field]
            errors = list(validator.iter_errors(env))
            assert errors, f"missing required 33GOD extension {field!r} should fail"

    def test_data_required(self, validator) -> None:
        env = _canonical_envelope()
        del env["data"]
        assert list(validator.iter_errors(env)), "missing data should fail"

    def test_matches_shape_dapr_preserves(self, validator) -> None:
        """Sanity: every field the bloodbank smoketest verifies Dapr preserves is
        representable in this envelope.
        """
        preserved_by_dapr = {
            "specversion", "id", "source", "type", "subject", "time",
            "datacontenttype", "dataschema", "correlationid", "causationid",
            "producer", "service", "domain", "schemaref", "traceparent", "data",
        }
        schema = json.loads(BASE_SCHEMA_PATH.read_text())
        declared = set(schema["properties"].keys())
        missing = preserved_by_dapr - declared
        assert not missing, f"envelope missing fields Dapr is known to preserve: {sorted(missing)}"

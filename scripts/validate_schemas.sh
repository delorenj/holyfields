#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCHEMA_DIR="$PROJECT_ROOT/schemas"

echo "🔎 Holyfields schema validation"
echo "Schema directory: $SCHEMA_DIR"

python3 - "$SCHEMA_DIR" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urljoin, urldefrag

from jsonschema import Draft202012Validator


def json_pointer_exists(doc: object, pointer: str) -> bool:
    if not pointer or pointer == "/":
        return True

    current = doc
    for raw_token in pointer.lstrip("/").split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            if not token.isdigit():
                return False
            index = int(token)
            if index >= len(current):
                return False
            current = current[index]
            continue
        if not isinstance(current, dict) or token not in current:
            return False
        current = current[token]
    return True


def iter_refs(node: object):
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str):
            yield ref
        for value in node.values():
            yield from iter_refs(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_refs(item)


schema_dir = Path(sys.argv[1])
schema_paths = sorted(schema_dir.rglob("*.json"))
if not schema_paths:
    raise SystemExit("No schemas found")

schemas_by_id: dict[str, dict] = {}
errors: list[str] = []

for path in schema_paths:
    rel = path.relative_to(schema_dir).as_posix()
    try:
        schema = json.loads(path.read_text())
    except Exception as exc:  # pragma: no cover
        errors.append(f"{rel}: failed to parse JSON: {exc}")
        continue

    schema_id = schema.get("$id")
    if not schema_id:
        errors.append(f"{rel}: missing $id")
        continue
    if schema_id in schemas_by_id:
        errors.append(f"{rel}: duplicate $id {schema_id}")
        continue

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        errors.append(f"{rel}: invalid Draft 2020-12 schema: {exc}")
        continue

    schemas_by_id[schema_id] = schema

for path in schema_paths:
    rel = path.relative_to(schema_dir).as_posix()
    schema = json.loads(path.read_text())
    base_uri = schema.get("$id")
    if not base_uri:
        continue

    for ref in iter_refs(schema):
        if ref.startswith("#"):
            _, fragment = urldefrag(ref)
            if fragment and not json_pointer_exists(schema, fragment):
                errors.append(f"{rel}: unresolved internal ref {ref}")
            continue

        target_uri, fragment = urldefrag(urljoin(base_uri, ref))
        target_schema = schemas_by_id.get(target_uri)
        if target_schema is None:
            errors.append(f"{rel}: unresolved external ref {ref} -> {target_uri}")
            continue
        if fragment and not json_pointer_exists(target_schema, fragment):
            errors.append(f"{rel}: unresolved fragment {ref} -> #{fragment}")

if errors:
    print("")
    print("❌ Schema validation failed")
    for error in errors:
        print(f" - {error}")
    raise SystemExit(1)

print("")
print(f"✅ Validated {len(schema_paths)} schema files")
print(f"✅ Registered {len(schemas_by_id)} schema IDs")
PY

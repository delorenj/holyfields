#!/usr/bin/env python3
"""Generate Pydantic v2 models from Holyfields JSON Schemas.

Simple, reliable generator that:
1. Reads each schema file
2. Resolves $ref to _common types
3. Generates a Pydantic BaseModel class per schema
4. Outputs one .py file per schema

Usage: python scripts/generate_pydantic.py
"""
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_DIR = Path(__file__).parent.parent / "schemas"
OUTPUT_DIR = Path(__file__).parent.parent / "src" / "holyfields" / "generated" / "python"

# Map JSON Schema types to Python types
TYPE_MAP = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "array": "list",
    "object": "dict",
    "null": "None",
}

# Known $defs from _common/types.v1.json
COMMON_TYPE_MAP = {
    "uuid": "str",
    "timestamp": "str",
    "semantic_version": "str",
    "agent_name": "str",
    "session_key": "str",
    "model_name": "str",
    "channel_type": "str",
}


def schema_to_class_name(rel_path: str) -> str:
    """Convert schema path to PascalCase class name.
    
    e.g. agent/error.v1.json → AgentErrorV1
         theboard/meeting.created.v1.json → TheboardMeetingCreatedV1
    """
    name = rel_path.replace(".json", "").replace("/", "_").replace(".", "_")
    # PascalCase
    return "".join(word.capitalize() for word in name.split("_"))


def resolve_type(prop: dict, prop_name: str) -> str:
    """Convert a JSON Schema property to a Python type annotation."""
    if "$ref" in prop:
        ref = prop["$ref"]
        # Handle _common/types.v1.json#/$defs/xxx
        if "#/$defs/" in ref:
            def_name = ref.split("#/$defs/")[-1]
            return COMMON_TYPE_MAP.get(def_name, "Any")
        # Handle base_event.v1.json reference (skip — it's the parent)
        if "base_event" in ref:
            return "__BASE__"
        if "theboard_extension" in ref:
            return "__EXTENSION__"
        return "Any"

    schema_type = prop.get("type", "any")

    if schema_type == "array":
        items = prop.get("items", {})
        item_type = resolve_type(items, prop_name)
        return f"list[{item_type}]"

    if schema_type == "object":
        additional = prop.get("additionalProperties")
        if additional and isinstance(additional, dict):
            val_type = resolve_type(additional, prop_name)
            return f"dict[str, {val_type}]"
        return "dict[str, Any]"

    if isinstance(schema_type, list):
        # Union type, e.g. ["string", "null"]
        types = [TYPE_MAP.get(t, "Any") for t in schema_type]
        return " | ".join(types)

    return TYPE_MAP.get(schema_type, "Any")


def extract_properties(schema: dict) -> list[tuple[str, str, bool, Any]]:
    """Extract (name, type, required, default) tuples from schema properties.
    
    Handles allOf composition by merging properties from all sub-schemas.
    """
    properties = {}
    required_fields = set(schema.get("required", []))

    # Direct properties
    if "properties" in schema:
        properties.update(schema["properties"])

    # allOf composition — merge properties from each sub-schema
    for sub in schema.get("allOf", []):
        if "properties" in sub:
            properties.update(sub["properties"])
            required_fields.update(sub.get("required", []))
        # Skip $ref to base_event (handled as parent class)

    fields = []
    for name, prop in properties.items():
        # Skip internal schema fields
        if name.startswith("$"):
            continue

        py_type = resolve_type(prop, name)
        if py_type in ("__BASE__", "__EXTENSION__"):
            continue

        is_required = name in required_fields
        default = prop.get("default")

        # Handle enum
        if "enum" in prop:
            # Use Literal type
            enum_vals = prop["enum"]
            if all(isinstance(v, str) for v in enum_vals):
                literals = ", ".join(f'"{v}"' for v in enum_vals)
                py_type = f"Literal[{literals}]"

        fields.append((name, py_type, is_required, default))

    return fields


def generate_nested_model(name: str, props: dict, required: set, indent: str = "") -> tuple[list[str], list[str]]:
    """Generate a nested Pydantic model class for object-type properties.
    
    Returns (model_lines, field_lines) where model_lines define the nested
    class and field_lines reference it.
    """
    model_lines = []
    class_name = "".join(word.capitalize() for word in name.split("_"))

    model_lines.append(f"{indent}class {class_name}(BaseModel):")
    
    has_fields = False
    for prop_name, prop in props.items():
        if prop_name.startswith("$"):
            continue
        
        py_type = resolve_type(prop, prop_name)
        if py_type in ("__BASE__", "__EXTENSION__"):
            continue
        
        # Recursively handle nested objects with properties
        if prop.get("type") == "object" and "properties" in prop:
            nested_required = set(prop.get("required", []))
            nested_models, _ = generate_nested_model(
                prop_name, prop["properties"], nested_required, indent + "    "
            )
            model_lines.extend(nested_models)
            py_type = "".join(word.capitalize() for word in prop_name.split("_"))
        
        is_required = prop_name in required
        # Sanitize: leading underscores not allowed in Pydantic, keywords need suffix
        field_name = prop_name
        if field_name.startswith("_"):
            field_name = field_name.lstrip("_")
        if field_name in ("type", "class", "from", "import", "in", "is", "not", "and", "or"):
            field_name = f"{field_name}_"
        needs_alias = field_name != prop_name
        desc = prop.get("description", "")
        
        alias_part = f', alias="{prop_name}"' if needs_alias else ""
        if is_required:
            if desc or needs_alias:
                model_lines.append(f'{indent}    {field_name}: {py_type} = Field(...{alias_part}, description="{desc}")')
            else:
                model_lines.append(f"{indent}    {field_name}: {py_type}")
        else:
            if desc or needs_alias:
                model_lines.append(f'{indent}    {field_name}: Optional[{py_type}] = Field(None{alias_part}, description="{desc}")')
            else:
                model_lines.append(f"{indent}    {field_name}: Optional[{py_type}] = None")
        has_fields = True
    
    if not has_fields:
        model_lines.append(f"{indent}    pass")
    
    model_lines.append("")
    return model_lines, class_name


def generate_model(rel_path: str, schema: dict) -> str:
    """Generate Pydantic model code for a single schema."""
    class_name = schema_to_class_name(rel_path)
    title = schema.get("title", rel_path)
    description = schema.get("description", "")

    # Build imports
    imports = [
        "from __future__ import annotations",
        "",
        "from typing import Any, Literal, Optional",
        "",
        "from pydantic import BaseModel, Field",
    ]

    lines = []
    
    # Check for payload with properties — generate a typed Payload model
    payload_prop = schema.get("properties", {}).get("payload", {})
    payload_class_name = None
    if payload_prop.get("type") == "object" and "properties" in payload_prop:
        payload_required = set(payload_prop.get("required", []))
        payload_model_lines, payload_class_name = generate_nested_model(
            "Payload", payload_prop["properties"], payload_required
        )
        lines.append("")
        lines.extend(payload_model_lines)

    # Main event class
    lines.append("")
    lines.append(f"class {class_name}(BaseModel):")
    if description:
        lines.append(f'    """{description}"""')
    elif title:
        lines.append(f'    """{title}"""')
    lines.append("")

    # event_type field (usually const)
    event_type_prop = schema.get("properties", {}).get("event_type", {})
    if "const" in event_type_prop:
        const_val = event_type_prop["const"]
        lines.append(f'    event_type: Literal["{const_val}"] = "{const_val}"')
    else:
        lines.append("    event_type: str")

    # payload field — typed or dict
    if payload_class_name:
        lines.append(f"    payload: {payload_class_name}")
    elif "payload" in schema.get("properties", {}):
        lines.append("    payload: dict[str, Any]")

    # Any other top-level properties (besides event_type, payload)
    all_props = schema.get("properties", {})
    for sub in schema.get("allOf", []):
        if "properties" in sub:
            all_props.update(sub["properties"])
    
    required_fields = set(schema.get("required", []))
    for sub in schema.get("allOf", []):
        required_fields.update(sub.get("required", []))

    for prop_name, prop in all_props.items():
        if prop_name in ("event_type", "payload", "$schema", "$id"):
            continue
        py_type = resolve_type(prop, prop_name)
        if py_type in ("__BASE__", "__EXTENSION__"):
            continue
        field_name = f"{prop_name}_" if prop_name in ("type", "class", "from", "import") else prop_name
        is_required = prop_name in required_fields
        if is_required:
            lines.append(f"    {field_name}: {py_type}")
        else:
            lines.append(f"    {field_name}: Optional[{py_type}] = None")

    return "\n".join(imports + lines) + "\n"


def main():
    print(f"🔨 Holyfields Pydantic Generator")
    print(f"Schema directory: {SCHEMA_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    
    # Clean output
    if OUTPUT_DIR.exists():
        import shutil
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Find all v1 schema files (skip _common)
    schema_files = sorted(SCHEMA_DIR.rglob("*.v1.json"))
    schema_files = [f for f in schema_files if "_common" not in str(f)]

    print(f"Found {len(schema_files)} event schemas")

    generated = 0
    failed = 0
    all_models = []  # (module_path, class_name) for __init__.py

    for schema_path in schema_files:
        rel_path = str(schema_path.relative_to(SCHEMA_DIR))
        
        try:
            schema = json.loads(schema_path.read_text())
            code = generate_model(rel_path, schema)

            # Output path mirrors schema structure
            out_name = rel_path.replace(".json", "").replace(".", "_") + ".py"
            out_path = OUTPUT_DIR / out_name
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(code)

            # Create __init__.py in subdirs
            init_path = out_path.parent / "__init__.py"
            if not init_path.exists():
                init_path.write_text("")

            class_name = schema_to_class_name(rel_path)
            module_path = out_name.replace("/", ".").replace(".py", "")
            all_models.append((module_path, class_name))

            print(f"  ✅ {rel_path} → {class_name}")
            generated += 1
        except Exception as e:
            print(f"  ❌ {rel_path}: {e}")
            failed += 1

    # Write root __init__.py with all re-exports
    init_lines = [
        '"""Holyfields generated Python contracts (v1).',
        "",
        "DO NOT EDIT MANUALLY. Generated from JSON Schemas.",
        'To regenerate: python scripts/generate_pydantic.py',
        '"""',
        "",
        "__version__ = '1.0.0'",
        "",
    ]
    for module_path, class_name in sorted(all_models):
        init_lines.append(f"from .{module_path} import {class_name}")

    init_lines.append("")
    init_lines.append("__all__ = [")
    for _, class_name in sorted(all_models):
        init_lines.append(f'    "{class_name}",')
    init_lines.append("]")
    init_lines.append("")

    (OUTPUT_DIR / "__init__.py").write_text("\n".join(init_lines))

    print(f"\n✅ Generated {generated} models ({failed} failed)")
    print(f"📁 Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

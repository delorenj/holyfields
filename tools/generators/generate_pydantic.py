#!/usr/bin/env python3
"""Generate Pydantic v2 models from Holyfields JSON Schemas."""

from __future__ import annotations

import json
import keyword
import re
import shutil
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "schemas"
OUTPUT_DIR = REPO_ROOT / "packages" / "python" / "src" / "holyfields" / "generated"
PACKAGE_SCHEMA_DIR = REPO_ROOT / "packages" / "python" / "src" / "holyfields" / "schemas"

TYPE_MAP = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "null": "None",
}

COMMON_TYPE_MAP = {
    "uuid": "str",
    "timestamp": "str",
    "semantic_version": "str",
    "agent_name": "str",
    "session_key": "str",
    "model_name": "str",
    "channel_type": "str",
}


def pascal(value: str) -> str:
    parts = re.split(r"[^A-Za-z0-9]+", value)
    return "".join(part[:1].upper() + part[1:] for part in parts if part)


def schema_to_class_name(rel_path: str) -> str:
    stem = rel_path.removesuffix(".json")
    return pascal(stem)


def schema_to_module_path(rel_path: str) -> str:
    return rel_path.removesuffix(".json").replace(".", "_") + ".py"


def resolve_ref_path(ref: str, current_schema_path: Path) -> Path | None:
    ref_path = ref.split("#", 1)[0]
    if not ref_path:
        return None
    if ref_path.startswith("https://33god.dev/schemas/"):
        return SCHEMA_DIR / ref_path.split("/schemas/", 1)[1]
    return (current_schema_path.parent / ref_path).resolve()


def load_ref(ref: str, current_schema_path: Path) -> dict[str, Any] | None:
    path = resolve_ref_path(ref, current_schema_path)
    if path is None:
        return None
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        return None
    return data


def merge_schema(schema: dict[str, Any], schema_path: Path) -> dict[str, Any]:
    """Merge top-level allOf refs with local properties for model generation."""
    merged: dict[str, Any] = {
        "title": schema.get("title"),
        "description": schema.get("description"),
        "type": schema.get("type", "object"),
        "properties": {},
        "required": [],
    }

    def merge_into(source: dict[str, Any], source_path: Path) -> None:
        for item in source.get("allOf", []):
            if "$ref" in item:
                ref_schema = load_ref(item["$ref"], source_path)
                if ref_schema:
                    merge_into(ref_schema, resolve_ref_path(item["$ref"], source_path) or source_path)
            else:
                merge_into(item, source_path)

        merged["properties"].update(source.get("properties", {}))
        merged["required"] = sorted(set(merged["required"]) | set(source.get("required", [])))
        if source.get("additionalProperties") is False:
            merged["additionalProperties"] = False

    merge_into(schema, schema_path)
    return merged


def field_name_for(name: str) -> tuple[str, str | None]:
    field_name = name.lstrip("_") or "field"
    if keyword.iskeyword(field_name):
        field_name = f"{field_name}_"
    return field_name, name if field_name != name else None


def literal(values: list[Any]) -> str:
    return "Literal[" + ", ".join(repr(value) for value in values) + "]"


def field_args(prop: dict[str, Any], alias: str | None) -> list[str]:
    args: list[str] = []
    if alias:
        args.append(f"alias={alias!r}")
    if description := prop.get("description"):
        args.append(f"description={description!r}")
    if "minimum" in prop:
        args.append(f"ge={prop['minimum']!r}")
    if "maximum" in prop:
        args.append(f"le={prop['maximum']!r}")
    if "minLength" in prop:
        args.append(f"min_length={prop['minLength']!r}")
    if "maxLength" in prop:
        args.append(f"max_length={prop['maxLength']!r}")
    if "minItems" in prop:
        args.append(f"min_length={prop['minItems']!r}")
    if "maxItems" in prop:
        args.append(f"max_length={prop['maxItems']!r}")
    if "pattern" in prop:
        args.append(f"pattern={prop['pattern']!r}")
    return args


class ModuleBuilder:
    def __init__(self, root_class_name: str) -> None:
        self.root_class_name = root_class_name
        self.nested_classes: list[str] = []
        self.used_class_names = {root_class_name}

    def unique_class_name(self, requested: str) -> str:
        candidate = requested
        suffix = 2
        while candidate in self.used_class_names:
            candidate = f"{requested}{suffix}"
            suffix += 1
        self.used_class_names.add(candidate)
        return candidate

    def type_for(self, prop: dict[str, Any], name: str, prefix: str) -> str:
        if "$ref" in prop:
            ref = prop["$ref"]
            if "#/$defs/" in ref:
                return COMMON_TYPE_MAP.get(ref.rsplit("/", 1)[-1], "Any")
            return "Any"

        if "const" in prop:
            return literal([prop["const"]])

        if "enum" in prop:
            return literal(prop["enum"])

        if "anyOf" in prop or "oneOf" in prop:
            options = prop.get("anyOf", prop.get("oneOf", []))
            types = [self.type_for(option, name, prefix) for option in options]
            return " | ".join(dict.fromkeys(types)) or "Any"

        schema_type = prop.get("type", "object" if "properties" in prop else "any")
        if isinstance(schema_type, list):
            types = [TYPE_MAP.get(item, "Any") for item in schema_type]
            return " | ".join(dict.fromkeys(types)) or "Any"

        if schema_type == "array":
            item_type = self.type_for(prop.get("items", {}), f"{name}_item", prefix)
            return f"list[{item_type}]"

        if schema_type == "object":
            if "properties" in prop:
                class_name = self.unique_class_name(f"{prefix}{pascal(name)}")
                self.add_model(class_name, prop)
                return class_name
            additional = prop.get("additionalProperties")
            if isinstance(additional, dict):
                value_type = self.type_for(additional, f"{name}_value", prefix)
                return f"dict[str, {value_type}]"
            return "dict[str, Any]"

        return TYPE_MAP.get(schema_type, "Any")

    def add_model(self, class_name: str, schema: dict[str, Any]) -> None:
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))
        lines: list[str] = [f"class {class_name}(BaseModel):"]

        if description := schema.get("description"):
            lines.append(f'    """{description}"""')
            lines.append("")

        if schema.get("additionalProperties") is False:
            lines.append('    model_config = ConfigDict(extra="forbid")')
            lines.append("")

        if not properties:
            lines.append("    pass")
        else:
            field_lines: list[str] = []
            for json_name, prop in properties.items():
                py_name, alias = field_name_for(json_name)
                py_type = self.type_for(prop, json_name, class_name)
                args = field_args(prop, alias)

                if json_name in required:
                    default = "..."
                elif "default" in prop:
                    default = repr(prop["default"])
                else:
                    default = "None"
                    if "None" not in py_type:
                        py_type = f"{py_type} | None"

                if args:
                    field_lines.append(
                        f"    {py_name}: {py_type} = Field({default}, {', '.join(args)})"
                    )
                elif default == "...":
                    field_lines.append(f"    {py_name}: {py_type}")
                else:
                    field_lines.append(f"    {py_name}: {py_type} = {default}")

            lines.extend(field_lines)

        lines.append("")
        self.nested_classes.append("\n".join(lines))


def generate_model(rel_path: str, schema_path: Path, schema: dict[str, Any]) -> str:
    class_name = schema_to_class_name(rel_path)
    merged = merge_schema(schema, schema_path)
    builder = ModuleBuilder(class_name)
    builder.add_model(class_name, merged)

    const_value = None
    for candidate in ("event_type", "type"):
        prop = merged.get("properties", {}).get(candidate, {})
        if "const" in prop:
            const_value = prop["const"]
            break

    root_model = builder.nested_classes.pop()
    if const_value:
        root_lines = root_model.rstrip().splitlines()
        if root_lines[-1] == "    pass":
            root_lines[-1] = f"    EVENT_TYPE: ClassVar[str] = {const_value!r}"
        else:
            root_lines.extend(["", f"    EVENT_TYPE: ClassVar[str] = {const_value!r}"])
        root_model = "\n".join(root_lines) + "\n"

    imports = [
        "from __future__ import annotations",
        "",
        "from typing import Any, ClassVar, Literal",
        "",
        "from pydantic import BaseModel, ConfigDict, Field",
        "",
    ]

    return "\n".join(imports + builder.nested_classes + [root_model]) + "\n"


def write_package_inits(generated: list[tuple[str, str]]) -> None:
    dirs = {OUTPUT_DIR}
    for path in OUTPUT_DIR.rglob("*.py"):
        dirs.add(path.parent)
    for directory in dirs:
        init = directory / "__init__.py"
        if not init.exists():
            init.write_text("")

    init_lines = [
        '"""Holyfields generated Python contracts.',
        "",
        "DO NOT EDIT MANUALLY. Generated from JSON Schemas.",
        'To regenerate: mise run generate:python',
        '"""',
        "",
    ]
    for module_path, class_name in sorted(generated):
        init_lines.append(f"from .{module_path} import {class_name}")

    init_lines.extend(["", "__all__ = ["])
    for _, class_name in sorted(generated):
        init_lines.append(f'    "{class_name}",')
    init_lines.extend(["]", ""])
    (OUTPUT_DIR / "__init__.py").write_text("\n".join(init_lines))


def sync_package_schemas() -> None:
    if PACKAGE_SCHEMA_DIR.exists():
        shutil.rmtree(PACKAGE_SCHEMA_DIR)
    shutil.copytree(SCHEMA_DIR, PACKAGE_SCHEMA_DIR)


def main() -> None:
    print("Holyfields Pydantic generator")
    print(f"Schema directory: {SCHEMA_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    schema_files = [
        path for path in sorted(SCHEMA_DIR.rglob("*.v1.json")) if "_common" not in path.parts
    ]
    generated: list[tuple[str, str]] = []

    for schema_path in schema_files:
        rel_path = schema_path.relative_to(SCHEMA_DIR).as_posix()
        schema = json.loads(schema_path.read_text())
        code = generate_model(rel_path, schema_path, schema)
        module_path = schema_to_module_path(rel_path)
        output_path = OUTPUT_DIR / module_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(code)
        class_name = schema_to_class_name(rel_path)
        generated.append((module_path.removesuffix(".py").replace("/", "."), class_name))
        print(f"  generated {rel_path} -> {class_name}")

    write_package_inits(generated)
    sync_package_schemas()
    print(f"Generated {len(generated)} Python models")
    print(f"Synced schemas into {PACKAGE_SCHEMA_DIR}")


if __name__ == "__main__":
    main()

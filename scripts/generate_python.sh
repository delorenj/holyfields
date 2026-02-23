#!/usr/bin/env bash
set -euo pipefail

# Generate Python Pydantic v2 models from Holyfields JSON Schemas
# Generates one .py file per schema in a mirrored directory structure

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCHEMA_DIR="$PROJECT_ROOT/schemas"
OUTPUT_DIR="$PROJECT_ROOT/src/holyfields/generated/python"

echo "🔨 Holyfields Python Generator (per-schema output)"
echo "Schema directory: $SCHEMA_DIR"
echo "Output directory: $OUTPUT_DIR"

# Require datamodel-codegen
if ! command -v datamodel-codegen &>/dev/null; then
  echo "❌ datamodel-codegen not found. Install: pip install datamodel-code-generator"
  exit 1
fi

# Clean and create output directories
echo "🧹 Cleaning output directory..."
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Find all v1 schema files (skip _common)
echo "📦 Discovering v1 schemas..."
SCHEMA_FILES=$(find "$SCHEMA_DIR" -name "*.v1.json" -type f -not -path "*/_common/*" | sort)
TOTAL=$(echo "$SCHEMA_FILES" | wc -l)
echo "Found $TOTAL event schemas (excluding _common)"

GENERATED=0
FAILED=0

while IFS= read -r schema_path; do
  # Relative path from schemas dir: e.g. agent/error.v1.json
  rel_path="${schema_path#$SCHEMA_DIR/}"
  # Output path: agent/error_v1.py
  out_name="${rel_path%.json}"
  out_name="${out_name//./_}"  # dots → underscores
  out_path="$OUTPUT_DIR/${out_name}.py"
  out_dir="$(dirname "$out_path")"

  mkdir -p "$out_dir"

  # Generate with datamodel-codegen
  if datamodel-codegen \
    --input "$schema_path" \
    --output "$out_path" \
    --input-file-type jsonschema \
    --output-model-type pydantic_v2.BaseModel \
    --target-python-version 3.12 \
    --use-annotated \
    --use-double-quotes \
    --collapse-root-models \
    --disable-timestamp \
    2>/dev/null; then
    echo "  ✅ $rel_path → ${out_name}.py"
    ((GENERATED++)) || true

    # Create __init__.py in each subdirectory
    if [ ! -f "$out_dir/__init__.py" ]; then
      touch "$out_dir/__init__.py"
    fi
  else
    echo "  ❌ $rel_path (generation failed)"
    ((FAILED++)) || true
  fi
done <<< "$SCHEMA_FILES"

# Create root __init__.py with re-exports
cat > "$OUTPUT_DIR/__init__.py" << 'EOF'
"""Holyfields generated Python contracts (v1).

DO NOT EDIT MANUALLY. Generated from JSON Schemas.
To regenerate: bash scripts/generate_python.sh
"""

__version__ = "1.0.0"
EOF

echo ""
echo "✅ Generation complete: $GENERATED succeeded, $FAILED failed out of $TOTAL schemas"
echo "📁 Output: $OUTPUT_DIR"

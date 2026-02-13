#!/usr/bin/env bash
set -euo pipefail

# Generate Python Pydantic models from JSON Schemas
# Updated for v1 schema structure with nested directories

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCHEMA_DIR="$PROJECT_ROOT/schemas"
OUTPUT_DIR="$PROJECT_ROOT/src/holyfields/generated/python"

echo "🔨 Holyfields Python Generator (v1 schema structure)"
echo "Schema directory: $SCHEMA_DIR"
echo "Output directory: $OUTPUT_DIR"

# Activate virtual environment if it exists
if [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
  source "$PROJECT_ROOT/.venv/bin/activate"
fi

# Clean and create output directories
echo "🧹 Cleaning output directory..."
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Find all v1 schema files
echo "📦 Discovering v1 schemas..."
SCHEMA_FILES=$(find "$SCHEMA_DIR" -name "*.v1.json" -type f | sort)

echo "Found $(echo "$SCHEMA_FILES" | wc -l) schema files"

# Generate all schemas with resolved references
echo "🏗️  Generating Pydantic models..."

# Build input arguments for datamodel-codegen
INPUT_ARGS=""
for schema_file in $SCHEMA_FILES; do
  INPUT_ARGS="$INPUT_ARGS --input $schema_file"
done

datamodel-codegen \
  $INPUT_ARGS \
  --input-file-type jsonschema \
  --output "$OUTPUT_DIR" \
  --output-model-type pydantic_v2.BaseModel \
  --field-constraints \
  --use-standard-collections \
  --use-schema-description \
  --use-field-description \
  --use-default \
  --use-double-quotes \
  --target-python-version 3.12 \
  --validation \
  --collapse-root-models \
  --disable-timestamp \
  2>&1 | grep -v "FutureWarning" || true

echo "📝 Creating package structure..."

# Create __init__.py with exports
cat > "$OUTPUT_DIR/__init__.py" <> 'EOF'
"""Holyfields generated Python contracts (v1).

DO NOT EDIT MANUALLY. Generated from JSON Schemas.
To regenerate: mise run generate:python
"""

# Re-export all generated models
# Individual imports will be added here by the generator

__version__ = "1.0.0"
EOF

echo "✅ Python code generation complete!"
echo "📁 Generated files in: $OUTPUT_DIR"
echo ""
echo "Next steps:"
echo "  1. Review generated models"
echo "  2. Update Bloodbank to import from holyfields.generated.python"
echo ""

# Optional: Run mypy validation
if command -v mypy &> /dev/null; then
  echo "🔍 Running mypy validation..."
  cd "$PROJECT_ROOT"
  mypy "$OUTPUT_DIR" --ignore-missing-imports || {
    echo "⚠️  Mypy validation found issues (non-fatal)"
  }
else
  echo "ℹ️  Mypy not found, skipping type validation"
fi

echo "✨ Done!"

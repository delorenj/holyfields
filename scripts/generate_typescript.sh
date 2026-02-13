#!/usr/bin/env bash
set -euo pipefail

# Generate TypeScript Zod schemas from JSON Schemas
# Updated for v1 schema structure with nested directories

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCHEMA_DIR="$PROJECT_ROOT/schemas"
OUTPUT_DIR="$PROJECT_ROOT/generated/typescript"

echo "🔨 Holyfields TypeScript Generator (v1 schema structure)"
echo "Schema directory: $SCHEMA_DIR"
echo "Output directory: $OUTPUT_DIR"

# Clean and create output directories
echo "🧹 Cleaning output directory..."
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Generate base types first
echo "📦 Generating base types..."

# Generate _common types
mkdir -p "$OUTPUT_DIR/_common"
bunx json-schema-to-zod \
  --input "$SCHEMA_DIR/_common/base_event.v1.json" \
  --output "$OUTPUT_DIR/_common/base_event.v1.ts" \
  --name "BaseEvent" \
  --type "BaseEvent" \
  --module esm \
  --withJsdocs 2>&1 || echo "⚠️  Base event generation had issues"

# Generate all domain schemas
echo "📦 Generating domain schemas..."

# Function to generate TypeScript from JSON schema
generate_ts() {
  local input_file="$1"
  local output_file="${input_file%.json}.ts"
  output_file="${output_file/$SCHEMA_DIR/$OUTPUT_DIR}"
  
  # Create output directory
  mkdir -p "$(dirname "$output_file")"
  
  # Get schema name from filename (e.g., "message.received.v1" -> "MessageReceived")
  local schema_name=$(basename "$input_file" .v1.json)
  schema_name=$(echo "$schema_name" | sed -E 's/(^|\.)([a-z])/\U\2/g' | sed 's/\.//g')
  
  bunx json-schema-to-zod \
    --input "$input_file" \
    --output "$output_file" \
    --name "${schema_name}EventSchema" \
    --type "${schema_name}Event" \
    --module esm \
    --withJsdocs 2>&1 || echo "⚠️  Failed to generate $schema_name"
}

# Find and generate all v1 schemas
find "$SCHEMA_DIR" -name "*.v1.json" -not -path "*/_common/*" | while read -r schema_file; do
  generate_ts "$schema_file"
done

echo "🔧 Post-processing..."

# Remove .unique() calls (Zod doesn't support uniqueItems)
find "$OUTPUT_DIR" -name "*.ts" -type f -exec sed -i 's/\.unique()//g' {} \; 2>/dev/null || true

echo "📝 Creating barrel exports..."

# Create root index.ts
cat > "$OUTPUT_DIR/index.ts" <> 'EOF'
/**
 * Holyfields TypeScript contracts (v1)
 *
 * DO NOT EDIT MANUALLY. Generated from JSON Schemas.
 * To regenerate: mise run generate:typescript
 */

export * from './_common/base_event.v1.js';

// Domain exports will be added here
EOF

echo "✅ TypeScript code generation complete!"
echo "📁 Generated files in: $OUTPUT_DIR"
echo ""
echo "Next steps:"
echo "  1. Review generated Zod schemas"
echo "  2. Import from holyfields in your TypeScript projects"
echo ""

# Optional: Run TypeScript validation
if command -v tsc &> /dev/null && [ -f "$PROJECT_ROOT/tsconfig.json" ]; then
  echo "🔍 Running TypeScript validation..."
  cd "$PROJECT_ROOT"
  tsc --noEmit || echo "⚠️  TypeScript validation found issues"
else
  echo "ℹ️  TypeScript not configured, skipping validation"
fi

echo "✨ Done!"

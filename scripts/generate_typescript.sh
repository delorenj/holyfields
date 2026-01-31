#!/usr/bin/env bash
set -euo pipefail

# Generate TypeScript Zod schemas and types from JSON Schemas
# Uses json-schema-to-zod for contract generation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCHEMA_DIR="$PROJECT_ROOT"
OUTPUT_DIR="$PROJECT_ROOT/generated/typescript"

echo "🔨 Generating TypeScript Zod schemas from JSON Schemas..."
echo "Schema directory: $SCHEMA_DIR"
echo "Output directory: $OUTPUT_DIR"

# Clean and create output directories
echo "🧹 Cleaning output directory..."
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/theboard/events"

echo "📦 Generating base event schema..."
bunx json-schema-to-zod \
  --input "$SCHEMA_DIR/common/schemas/base_event.json" \
  --output "$OUTPUT_DIR/base_event.ts" \
  --name "baseEventSchema" \
  --type "BaseEvent" \
  --module esm \
  --withJsdocs

echo "📦 Generating TheBoard event schemas..."

# meeting_created.json
bunx json-schema-to-zod \
  --input "$SCHEMA_DIR/theboard/events/meeting_created.json" \
  --output "$OUTPUT_DIR/theboard/events/meeting_created.ts" \
  --name "meetingCreatedEventSchema" \
  --type "MeetingCreatedEvent" \
  --module esm \
  --withJsdocs

# meeting_started.json
bunx json-schema-to-zod \
  --input "$SCHEMA_DIR/theboard/events/meeting_started.json" \
  --output "$OUTPUT_DIR/theboard/events/meeting_started.ts" \
  --name "meetingStartedEventSchema" \
  --type "MeetingStartedEvent" \
  --module esm \
  --withJsdocs

# round_completed.json
bunx json-schema-to-zod \
  --input "$SCHEMA_DIR/theboard/events/round_completed.json" \
  --output "$OUTPUT_DIR/theboard/events/round_completed.ts" \
  --name "roundCompletedEventSchema" \
  --type "RoundCompletedEvent" \
  --module esm \
  --withJsdocs

# comment_extracted.json
bunx json-schema-to-zod \
  --input "$SCHEMA_DIR/theboard/events/comment_extracted.json" \
  --output "$OUTPUT_DIR/theboard/events/comment_extracted.ts" \
  --name "commentExtractedEventSchema" \
  --type "CommentExtractedEvent" \
  --module esm \
  --withJsdocs

# meeting_converged.json
bunx json-schema-to-zod \
  --input "$SCHEMA_DIR/theboard/events/meeting_converged.json" \
  --output "$OUTPUT_DIR/theboard/events/meeting_converged.ts" \
  --name "meetingConvergedEventSchema" \
  --type "MeetingConvergedEvent" \
  --module esm \
  --withJsdocs

# meeting_completed.json
bunx json-schema-to-zod \
  --input "$SCHEMA_DIR/theboard/events/meeting_completed.json" \
  --output "$OUTPUT_DIR/theboard/events/meeting_completed.ts" \
  --name "meetingCompletedEventSchema" \
  --type "MeetingCompletedEvent" \
  --module esm \
  --withJsdocs

# meeting_failed.json
bunx json-schema-to-zod \
  --input "$SCHEMA_DIR/theboard/events/meeting_failed.json" \
  --output "$OUTPUT_DIR/theboard/events/meeting_failed.ts" \
  --name "meetingFailedEventSchema" \
  --type "MeetingFailedEvent" \
  --module esm \
  --withJsdocs

echo "🔧 Post-processing generated files..."

# Remove .unique() calls (Zod doesn't support uniqueItems natively)
# Note: uniqueItems validation is enforced on Python side, not TypeScript runtime
find "$OUTPUT_DIR" -name "*.ts" -type f -exec sed -i 's/\.unique()//g' {} \;

# Fix format types and $ref types that json-schema-to-zod converts to z.any()
# Replace z.any() with proper Zod validators
find "$OUTPUT_DIR" -name "*.ts" -type f -exec sed -i \
  -e 's/z\.any()\.describe("ISO 8601 UTC timestamp when event was emitted")/z.string().datetime().describe("ISO 8601 UTC timestamp when event was emitted")/g' \
  -e 's/z\.any()\.describe("UUID of the meeting this event relates to\. Used for event correlation and tracing\.")/z.string().uuid().describe("UUID of the meeting this event relates to. Used for event correlation and tracing.")/g' \
  -e 's/z\.any()\.describe("Novelty score (0\.0 = repetitive, 1\.0 = novel)")/z.number().min(0.0).max(1.0).describe("Novelty score (0.0 = repetitive, 1.0 = novel)")/g' \
  {} \;

# Fix event schema composition
# Use baseEventSchema.extend() pattern to properly override event_type with specific literal
for file in "$OUTPUT_DIR/theboard/events/"*.ts; do
  if [[ "$file" != *"/index.ts" ]]; then
    # Add import for baseEventSchema at the top (after existing imports)
    sed -i '1 a import { baseEventSchema } from "../../base_event.js"' "$file"

    # Transform: z.object({ ...fields }).strict().and(z.any())
    # Into: baseEventSchema.extend({ ...fields })
    # This preserves event_type literals and properly composes with base
    sed -i -e 's/export const \([a-zA-Z]*\) = z\.object(/export const \1 = baseEventSchema.extend(/g' \
           -e 's/\.strict()\.and(z\.any())//g' "$file"
  fi
done

echo "📝 Creating barrel exports..."

# Create root index.ts
cat > "$OUTPUT_DIR/index.ts" <<'EOF'
/**
 * Holyfields TypeScript contracts
 *
 * DO NOT EDIT MANUALLY. Generated from JSON Schemas.
 * To regenerate: mise run generate:typescript
 */

export * from './base_event.js';
export * from './theboard/events/index.js';
EOF

# Create theboard/events/index.ts
cat > "$OUTPUT_DIR/theboard/events/index.ts" <<'EOF'
/**
 * TheBoard event schemas
 *
 * DO NOT EDIT MANUALLY. Generated from JSON Schemas.
 * Source: ~/code/33GOD/holyfields/trunk-main/theboard/events/*.json
 *
 * To regenerate: mise run generate:typescript
 */

export * from './meeting_created.js';
export * from './meeting_started.js';
export * from './round_completed.js';
export * from './comment_extracted.js';
export * from './meeting_converged.js';
export * from './meeting_completed.js';
export * from './meeting_failed.js';
EOF

echo "✅ TypeScript code generation complete!"
echo "📁 Generated files in: $OUTPUT_DIR"
echo ""
echo "Usage in theboardroom:"
echo "  import { meetingCreatedEventSchema, type MeetingCreatedEvent } from 'holyfields';"
echo ""
echo "🔍 Validate with: tsc --noEmit"

# Run TypeScript validation
if command -v tsc &> /dev/null; then
  echo ""
  echo "🔍 Running TypeScript validation..."
  cd "$PROJECT_ROOT"
  tsc --noEmit || {
    echo "⚠️  TypeScript validation found issues"
    exit 1
  }
  echo "✅ TypeScript validation passed!"
else
  echo ""
  echo "ℹ️  TypeScript not found in PATH, skipping validation"
fi

echo "✨ Done!"

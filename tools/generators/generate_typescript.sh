#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SCHEMA_DIR="$PROJECT_ROOT/schemas"
OUTPUT_DIR="$PROJECT_ROOT/packages/typescript/src/generated"

echo "Holyfields TypeScript generator"
echo "Schema directory: $SCHEMA_DIR"
echo "Output directory: $OUTPUT_DIR"

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

schema_name() {
  local rel="$1"
  python3 - "$rel" <<'PY'
from __future__ import annotations

import re
import sys

rel = sys.argv[1].removesuffix(".json")
parts = re.split(r"[^A-Za-z0-9]+", rel)
print("".join(part[:1].upper() + part[1:] for part in parts if part))
PY
}

generated_files=()

while IFS= read -r schema_file; do
  rel="${schema_file#$SCHEMA_DIR/}"
  output_file="$OUTPUT_DIR/${rel%.json}.ts"
  class_name="$(schema_name "$rel")"

  mkdir -p "$(dirname "$output_file")"
  bunx json-schema-to-zod \
    --input "$schema_file" \
    --output "$output_file" \
    --name "${class_name}Schema" \
    --type "$class_name" \
    --module esm \
    --withJsdocs

  generated_files+=("${rel%.json}.ts")
  echo "  generated $rel -> ${class_name}Schema"
done < <(find "$SCHEMA_DIR" -name "*.v1.json" | sort)

find "$OUTPUT_DIR" -name "*.ts" -type f -exec sed -i 's/\.unique()//g' {} \;

{
  cat <<'EOF'
/**
 * Holyfields generated TypeScript contracts.
 *
 * DO NOT EDIT MANUALLY. Generated from JSON Schemas.
 * To regenerate: mise run generate:typescript
 */

EOF
  for rel in "${generated_files[@]}"; do
    echo "export * from './${rel%.ts}.js';"
  done
} > "$OUTPUT_DIR/index.ts"

echo "Generated ${#generated_files[@]} TypeScript modules"

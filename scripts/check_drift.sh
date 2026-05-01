#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Schema drift check: regenerating all committed language artifacts"

bash "$PROJECT_ROOT/scripts/generate_python.sh"
bash "$PROJECT_ROOT/scripts/generate_typescript.sh"

cd "$PROJECT_ROOT"

if ! git diff --exit-code -- packages/python/src/holyfields/generated packages/python/src/holyfields/schemas packages/typescript/src/generated > /dev/null 2>&1; then
    echo ""
    echo "Schema drift detected"
    echo ""
    git diff --stat -- packages/python/src/holyfields/generated packages/python/src/holyfields/schemas packages/typescript/src/generated
    echo ""
    echo "Regenerate artifacts and commit the result:"
    echo "  mise run generate:all"
    exit 1
fi

echo "No schema drift detected"

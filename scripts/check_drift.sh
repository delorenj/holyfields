#!/usr/bin/env bash
set -euo pipefail

# Schema Drift Check
# Regenerates Pydantic models from JSON schemas and fails if any differ
# from the committed versions. This ensures schemas and generated code
# stay in sync.
#
# Usage: bash scripts/check_drift.sh
# Exit code: 0 = no drift, 1 = drift detected

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔍 Schema drift check: regenerating models..."

# Run the generator
python3 "$SCRIPT_DIR/generate_pydantic.py" 2>&1 | tail -3

# Check for differences
echo ""
echo "🔍 Checking for drift..."

cd "$PROJECT_ROOT"

if git diff --exit-code -- src/holyfields/generated/ > /dev/null 2>&1; then
    echo "✅ No schema drift detected — generated models match committed versions"
    exit 0
else
    echo ""
    echo "❌ SCHEMA DRIFT DETECTED"
    echo ""
    echo "The following generated files differ from the committed versions:"
    echo ""
    git diff --stat -- src/holyfields/generated/
    echo ""
    echo "This means JSON schemas were modified without regenerating Pydantic models."
    echo ""
    echo "To fix:"
    echo "  1. cd holyfields"
    echo "  2. python3 scripts/generate_pydantic.py"
    echo "  3. git add src/holyfields/generated/"
    echo "  4. git commit --amend (or new commit)"
    echo ""
    exit 1
fi

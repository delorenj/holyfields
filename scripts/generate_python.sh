#!/usr/bin/env bash
set -euo pipefail

# Public Python generation entrypoint.
# Keep this wrapper stable for docs/mise/CI, but delegate to the custom
# generator that matches the committed generated tree.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔨 Holyfields Python Generator"
echo "↪ delegating to scripts/generate_pydantic.py"

exec python3 "$SCRIPT_DIR/generate_pydantic.py"

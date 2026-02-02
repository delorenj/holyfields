#!/usr/bin/env bash
set -euo pipefail

# Generate Python Pydantic models from JSON Schemas
# Uses datamodel-code-generator for contract generation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCHEMA_DIR="$PROJECT_ROOT"
OUTPUT_DIR="$PROJECT_ROOT/src/holyfields/generated/python"

# Activate virtual environment if it exists
if [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
  source "$PROJECT_ROOT/.venv/bin/activate"
fi

echo "🔨 Generating Python Pydantic models from JSON Schemas..."
echo "Schema directory: $SCHEMA_DIR"
echo "Output directory: $OUTPUT_DIR"

# Clean and create output directories
echo "🧹 Cleaning output directory..."
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Generate all schemas into output directory (modular mode for $ref resolution)
echo "📦 Generating all schemas with resolved references..."
datamodel-codegen \
  --input "$SCHEMA_DIR/common/schemas" \
  --input "$SCHEMA_DIR/theboard/events" \
  --input "$SCHEMA_DIR/schemas/conversation" \
  --input "$SCHEMA_DIR/schemas/task" \
  --input "$SCHEMA_DIR/schemas/agent" \
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
  --collapse-root-models 2>&1 | grep -v "FutureWarning"

echo "📝 Creating package structure..."

# Create __init__.py for root package
# Note: BaseEvent is generated in comment_extracted.py due to datamodel-codegen behavior
cat > "$OUTPUT_DIR/__init__.py" <<'EOF'
"""Holyfields generated Python contracts.

DO NOT EDIT MANUALLY. Generated from JSON Schemas.
To regenerate: mise run generate:python
"""

from .comment_extracted import BaseEvent, CommentExtractedEvent
from .meeting_created import MeetingCreatedEvent
from .meeting_started import MeetingStartedEvent
from .round_completed import RoundCompletedEvent
from .meeting_converged import MeetingConvergedEvent
from .meeting_completed import MeetingCompletedEvent, TopComment
from .meeting_failed import MeetingFailedEvent
from .message_posted import MessagePostedEvent
from .step_proposed import TaskStepProposedEvent
from .step_executed import TaskStepExecutedEvent
from .state_changed import AgentStateChangedEvent

__all__ = [
    "BaseEvent",
    "MeetingCreatedEvent",
    "MeetingStartedEvent",
    "RoundCompletedEvent",
    "CommentExtractedEvent",
    "MeetingConvergedEvent",
    "MeetingCompletedEvent",
    "TopComment",
    "MeetingFailedEvent",
    "MessagePostedEvent",
    "TaskStepProposedEvent",
    "TaskStepExecutedEvent",
    "AgentStateChangedEvent",
]
EOF

# Create theboard package structure
mkdir -p "$OUTPUT_DIR/theboard/events"

cat > "$OUTPUT_DIR/theboard/__init__.py" <<'EOF'
"""TheBoard contract schemas.

DO NOT EDIT MANUALLY. Generated from JSON Schemas.
To regenerate: mise run generate:python
"""
EOF

cat > "$OUTPUT_DIR/theboard/events/__init__.py" <<'EOF'
"""TheBoard event schemas.

DO NOT EDIT MANUALLY. Generated from JSON Schemas.
Source: ~/code/33GOD/holyfields/trunk-main/theboard/events/*.json

To regenerate: mise run generate:python
"""

from ... import (
    MeetingCreatedEvent,
    MeetingStartedEvent,
    RoundCompletedEvent,
    CommentExtractedEvent,
    MeetingConvergedEvent,
    MeetingCompletedEvent,
    TopComment,
    MeetingFailedEvent,
)

__all__ = [
    "MeetingCreatedEvent",
    "MeetingStartedEvent",
    "RoundCompletedEvent",
    "CommentExtractedEvent",
    "MeetingConvergedEvent",
    "MeetingCompletedEvent",
    "TopComment",
    "MeetingFailedEvent",
]
EOF

echo "✅ Python code generation complete!"
echo "📁 Generated files in: $OUTPUT_DIR"
echo ""
echo "Usage in theboard:"
echo "  from holyfields.generated.python.theboard.events import MeetingCreatedEvent"
echo ""
echo "🔍 Validate with: mypy generated/python/"

# Run mypy validation
if command -v mypy &> /dev/null; then
  echo ""
  echo "🔍 Running mypy validation..."
  cd "$PROJECT_ROOT"
  mypy "$OUTPUT_DIR" --ignore-missing-imports || {
    echo "⚠️  Mypy validation found issues (non-fatal)"
    exit 1
  }
  echo "✅ Mypy validation passed!"
else
  echo ""
  echo "ℹ️  Mypy not found, skipping type validation"
fi

echo "✨ Done!"

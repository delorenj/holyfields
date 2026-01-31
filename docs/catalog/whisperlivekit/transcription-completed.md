# Transcription Completed Event

**Event Type:** `whisperlivekit.transcription.completed`
**Component:** WhisperLiveKit
**Version:** 1.0.0
**Status:** Ready for Integration

## Overview

Emitted by WhisperLiveKit when it completes transcription of an audio segment. This event is the primary trigger for the voice-to-response pipeline, notifying downstream consumers (like Tonny agent) that new transcribed text is available for processing.

## Event Flow

```
User speaks → WhisperLiveKit transcribes → Event published to Bloodbank
                                                 ↓
                                          Tonny agent consumes
                                                 ↓
                                          LLM processes request
                                                 ↓
                                          ElevenLabs TTS response
```

## Schema Definition

**Schema Location:** `whisperlivekit/events/transcription_completed.json`

### Required Fields

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `event_type` | string | Event discriminator (literal) | Must be `"whisperlivekit.transcription.completed"` |
| `timestamp` | string | ISO 8601 UTC timestamp | RFC 3339 format |
| `session_id` | string | Voice session UUID | RFC 4122 UUID |
| `source` | string | Component that emitted event | Pattern: `^[a-z0-9_-]+$` |
| `target` | string | Intended consumer | Pattern: `^[a-z0-9_-]+$` |
| `text` | string | Transcribed text | min: 1, max: 10000 characters |
| `audio_metadata` | object | Audio segment metadata | See Audio Metadata schema |
| `is_final` | boolean | Final vs partial transcription | Default: `true` |

### Optional Fields

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `segment_id` | string \| null | Unique segment identifier | Free-form string |

### Audio Metadata Object

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `duration_ms` | integer | Audio duration | >= 0 milliseconds |
| `sample_rate` | integer | Audio sample rate | 8000-48000 Hz |
| `channels` | integer | Number of channels | 1 (mono) or 2 (stereo) |
| `format` | enum | Audio format | `"pcm"`, `"wav"`, `"mp3"`, `"opus"` |
| `bit_depth` | integer \| null | Audio bit depth (optional) | 8, 16, 24, or 32 |
| `language` | string \| null | Language code (optional) | ISO 639-1 (e.g., `"en"`) |
| `confidence` | number \| null | Transcription confidence (optional) | 0.0-1.0 |

## Example Payloads

### Basic Transcription (Minimal)

```json
{
  "event_type": "whisperlivekit.transcription.completed",
  "timestamp": "2026-01-27T10:30:15.234Z",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "source": "whisperlivekit",
  "target": "tonny",
  "text": "Hey Tonny, what's the weather like today?",
  "audio_metadata": {
    "duration_ms": 2500,
    "sample_rate": 16000,
    "channels": 1,
    "format": "pcm"
  },
  "is_final": true
}
```

### Complete Transcription (With Metadata)

```json
{
  "event_type": "whisperlivekit.transcription.completed",
  "timestamp": "2026-01-27T10:30:15.234Z",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "source": "whisperlivekit",
  "target": "tonny",
  "text": "Hey Tonny, what's the weather like today?",
  "audio_metadata": {
    "duration_ms": 2500,
    "sample_rate": 16000,
    "channels": 1,
    "bit_depth": 16,
    "format": "pcm",
    "language": "en",
    "confidence": 0.95
  },
  "is_final": true,
  "segment_id": "seg_001"
}
```

### Partial/Streaming Transcription

```json
{
  "event_type": "whisperlivekit.transcription.completed",
  "timestamp": "2026-01-27T10:30:12.100Z",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "source": "whisperlivekit",
  "target": "candybar",
  "text": "Hey Tonny, what's the...",
  "audio_metadata": {
    "duration_ms": 1200,
    "sample_rate": 16000,
    "channels": 1,
    "format": "pcm",
    "confidence": 0.78
  },
  "is_final": false,
  "segment_id": "seg_001_partial"
}
```

## Usage in Python (Pydantic)

### Import

```python
from holyfields.generated.python.whisperlivekit.events import (
    TranscriptionCompletedEvent,
    AudioMetadata,
    Format,
    BitDepth,
)
```

### Creating an Event

```python
from datetime import datetime, timezone
from uuid import uuid4

# Create event
event = TranscriptionCompletedEvent(
    event_type="whisperlivekit.transcription.completed",
    timestamp=datetime.now(timezone.utc),
    session_id=uuid4(),
    source="whisperlivekit",
    target="tonny",
    text="Hey Tonny, what's the weather like today?",
    audio_metadata=AudioMetadata(
        duration_ms=2500,
        sample_rate=16000,
        channels=1,
        bit_depth=BitDepth.integer_16,
        format=Format.pcm,
        language="en",
        confidence=0.95,
    ),
    is_final=True,
    segment_id="seg_001",
)

# Serialize to JSON
json_str = event.model_dump_json()

# Publish to Bloodbank
# bb publish --event-type whisperlivekit.transcription.completed --payload '{...}'
```

### Validating an Event

```python
import json

# Parse from JSON
raw_json = '{"event_type": "whisperlivekit.transcription.completed", ...}'
event = TranscriptionCompletedEvent.model_validate_json(raw_json)

# Or from dict
raw_dict = json.loads(raw_json)
event = TranscriptionCompletedEvent.model_validate(raw_dict)

# Validation happens automatically - raises ValidationError if invalid
```

### Consuming from Bloodbank

```python
def handle_transcription_event(payload: dict) -> None:
    """Consumer callback for transcription events."""
    try:
        # Validate event against schema
        event = TranscriptionCompletedEvent.model_validate(payload)

        # Process transcription
        print(f"Received: {event.text}")
        print(f"Confidence: {event.audio_metadata.confidence}")
        print(f"Session: {event.session_id}")

        # Route to LLM for processing
        # ...

    except ValidationError as e:
        print(f"Invalid event payload: {e}")
```

## Usage in TypeScript (Zod)

### Import

```typescript
import {
  transcriptionCompletedEventSchema,
  type TranscriptionCompletedEvent
} from '@holyfields/generated/typescript/whisperlivekit/events';
```

### Validating an Event

```typescript
// Parse and validate from unknown data
const rawEvent = JSON.parse(messageBody);
const result = transcriptionCompletedEventSchema.safeParse(rawEvent);

if (result.success) {
  const event: TranscriptionCompletedEvent = result.data;
  console.log(`Transcription: ${event.text}`);
  console.log(`Confidence: ${event.audio_metadata.confidence}`);
} else {
  console.error('Validation failed:', result.error.errors);
}
```

### Creating an Event

```typescript
const event: TranscriptionCompletedEvent = {
  event_type: 'whisperlivekit.transcription.completed',
  timestamp: new Date().toISOString(),
  session_id: crypto.randomUUID(),
  source: 'whisperlivekit',
  target: 'tonny',
  text: "Hey Tonny, what's the weather like today?",
  audio_metadata: {
    duration_ms: 2500,
    sample_rate: 16000,
    channels: 1,
    bit_depth: 16,
    format: 'pcm',
    language: 'en',
    confidence: 0.95,
  },
  is_final: true,
  segment_id: 'seg_001',
};

// Validate before sending
const validated = transcriptionCompletedEventSchema.parse(event);
```

### React Component Example

```typescript
import { useEffect, useState } from 'react';
import { transcriptionCompletedEventSchema } from '@holyfields/generated/typescript/whisperlivekit/events';

function TranscriptionMonitor() {
  const [events, setEvents] = useState<TranscriptionCompletedEvent[]>([]);

  useEffect(() => {
    // Subscribe to Bloodbank events via WebSocket
    const ws = new WebSocket('ws://bloodbank/events');

    ws.onmessage = (msg) => {
      const result = transcriptionCompletedEventSchema.safeParse(JSON.parse(msg.data));

      if (result.success) {
        setEvents((prev) => [...prev, result.data]);
      } else {
        console.error('Invalid event:', result.error);
      }
    };

    return () => ws.close();
  }, []);

  return (
    <ul>
      {events.map((event) => (
        <li key={event.segment_id}>
          {event.text} ({event.audio_metadata.confidence?.toFixed(2)})
        </li>
      ))}
    </ul>
  );
}
```

## Integration with Bloodbank

### Publishing Events (WhisperLiveKit)

```bash
# Using bb CLI
bb publish \
  --event-type whisperlivekit.transcription.completed \
  --payload '{
    "event_type": "whisperlivekit.transcription.completed",
    "timestamp": "2026-01-27T10:30:15.234Z",
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "source": "whisperlivekit",
    "target": "tonny",
    "text": "Hey Tonny, what'\''s the weather like today?",
    "audio_metadata": {
      "duration_ms": 2500,
      "sample_rate": 16000,
      "channels": 1,
      "format": "pcm"
    },
    "is_final": true
  }'
```

### Subscribing to Events (Tonny Agent)

```bash
# Register as consumer
bb subscribe \
  --event-type whisperlivekit.transcription.completed \
  --target tonny \
  --callback http://tonny-service/webhooks/transcription
```

### Routing Rules

Events are routed based on:
1. **Event type**: `whisperlivekit.transcription.completed`
2. **Target field**: Specific consumer (e.g., `tonny`, `candybar`) or `all` for broadcast

## Testing

### Python Tests

```bash
# Run contract validation tests
pytest tests/python/test_transcription_events.py -v

# Expected: 16 tests pass, 99% coverage
```

### TypeScript Tests

```bash
# Run Zod schema tests
bun test tests/typescript/transcription_events.test.ts

# Expected: 19 tests pass
```

## Versioning and Compatibility

**Current Version:** 1.0.0
**Schema Versioning:** Semantic versioning applies to schema changes

- **Major version bump**: Breaking changes (field removal, type change, stricter constraints)
- **Minor version bump**: Additive changes (new optional field)
- **Patch version bump**: Documentation or example updates

### Backward Compatibility Guarantees

1. **No field removal** in minor/patch versions
2. **No type changes** in minor/patch versions
3. **Optional fields** can be added in minor versions
4. **Constraints can be relaxed** (e.g., max_length increase) in minor versions
5. **Deprecation warnings** before any breaking changes

## Related Events

- `whisperlivekit.transcription.partial` (planned) - Streaming partial results
- `tonny.response.completed` (planned) - TTS response after processing
- `tonny.error.transcription_failed` (planned) - Error handling

## Troubleshooting

### Common Validation Errors

**Error: `text` field is empty**
```python
# ❌ Invalid
event = TranscriptionCompletedEvent(..., text="")

# ✅ Valid
event = TranscriptionCompletedEvent(..., text="Hello")
```

**Error: Invalid `event_type` literal**
```python
# ❌ Invalid
event = TranscriptionCompletedEvent(event_type="wrong.type", ...)

# ✅ Valid (must match exactly)
event = TranscriptionCompletedEvent(
    event_type="whisperlivekit.transcription.completed",
    ...
)
```

**Error: `sample_rate` out of range**
```python
# ❌ Invalid (too low)
audio_metadata = AudioMetadata(sample_rate=4000, ...)

# ✅ Valid (8000-48000 Hz)
audio_metadata = AudioMetadata(sample_rate=16000, ...)
```

## Support and Questions

- **Schema Issues**: Open issue in `holyfields` repository
- **Integration Help**: Contact HolyFields EM or Bloodbank EM
- **Documentation Updates**: Submit PR to `docs/catalog/whisperlivekit/`

## Change Log

### v1.0.0 (2026-01-27)
- Initial schema definition
- Python Pydantic bindings
- TypeScript Zod bindings
- Comprehensive validation tests
- Documentation and examples

# EPIC-001: Transcription Event Schemas - COMPLETE

**Date:** 2026-01-27
**Owner:** HolyFields Engineering Manager
**Status:** ✅ READY FOR INTEGRATION

---

## 📦 Deliverables

### STORY-001: Define Transcription Event Schema ✅

**Schema Files Created:**

1. **Base Voice Event Schema**
   - Location: `common/schemas/base_voice_event.json`
   - Purpose: Shared base for all voice-related events
   - Fields: `event_type`, `timestamp`, `session_id`, `source`, `target`

2. **Transcription Completed Event Schema**
   - Location: `whisperlivekit/events/transcription_completed.json`
   - Event Type: `whisperlivekit.transcription.completed`
   - Extends: `base_voice_event.json`
   - Additional Fields:
     - `text` (string, 1-10000 chars): Transcribed text
     - `audio_metadata` (object): Audio segment metadata
     - `is_final` (boolean): Final vs partial transcription
     - `segment_id` (string, optional): Segment identifier

3. **Audio Metadata Schema**
   - Embedded in transcription event
   - Fields:
     - `duration_ms` (int, >=0): Audio duration
     - `sample_rate` (int, 8000-48000): Sample rate in Hz
     - `channels` (int, 1-2): Mono or stereo
     - `bit_depth` (enum, optional): 8, 16, 24, or 32
     - `format` (enum): pcm, wav, mp3, opus
     - `language` (string, optional): ISO 639-1 code
     - `confidence` (float, optional): 0.0-1.0 score

**Validation:** ✅ All schemas validated with JSON Schema Draft 2020-12

---

### STORY-002: Create Python/TypeScript Schema Bindings ✅

**Python Bindings (Pydantic v2)**

- Location: `src/holyfields/generated/python/whisperlivekit/events/`
- Files:
  - `transcription_completed.py` - Generated Pydantic models
  - `__init__.py` - Package exports
- Models:
  - `BaseVoiceEvent` - Base event model
  - `AudioMetadata` - Audio metadata model
  - `BitDepth` (IntEnum) - Bit depth enumeration
  - `Format` (StrEnum) - Audio format enumeration
  - `TranscriptionCompletedEvent` - Complete event model

**Import Example:**
```python
from holyfields.generated.python.whisperlivekit.events import (
    TranscriptionCompletedEvent,
    AudioMetadata,
    Format,
    BitDepth,
)
```

**TypeScript Bindings (Zod + TypeScript)**

- Location: `generated/typescript/whisperlivekit/events/`
- Files:
  - `transcription_completed.ts` - Zod schema + TypeScript type
  - `index.ts` - Package exports
- Exports:
  - `baseVoiceEventSchema` - Zod schema for base event
  - `transcriptionCompletedEventSchema` - Zod schema for event
  - `TranscriptionCompletedEvent` - TypeScript type

**Import Example:**
```typescript
import {
  transcriptionCompletedEventSchema,
  type TranscriptionCompletedEvent
} from '@holyfields/generated/typescript/whisperlivekit/events';
```

---

## 🧪 Testing and Validation

### Python Tests ✅

- Location: `tests/python/test_transcription_events.py`
- Framework: pytest + Pydantic
- Coverage: **16 tests, 99% coverage**
- Test suites:
  - `TestBaseVoiceEvent` (4 tests) - Base event validation
  - `TestAudioMetadata` (6 tests) - Audio metadata validation
  - `TestTranscriptionCompletedEvent` (6 tests) - Complete event validation

**Run Tests:**
```bash
cd ~/code/33GOD/holyfields/trunk-main
source .venv/bin/activate
pytest tests/python/test_transcription_events.py -v
```

**Expected Output:**
```
16 passed in 0.17s
Coverage: 99%
```

### TypeScript Tests ✅

- Location: `tests/typescript/transcription_events.test.ts`
- Framework: vitest + Zod
- Coverage: **19 tests, all passing**
- Test suites:
  - Valid Events (4 tests)
  - Invalid Events (13 tests)
  - Example Payloads (2 tests)

**Run Tests:**
```bash
cd ~/code/33GOD/holyfields/trunk-main
bun test tests/typescript/transcription_events.test.ts
```

**Expected Output:**
```
19 pass
0 fail
```

---

## 📚 Documentation

### Comprehensive Documentation Created ✅

**Location:** `docs/catalog/whisperlivekit/transcription-completed.md`

**Contents:**
- Event overview and flow diagram
- Complete field descriptions with constraints
- Example payloads (minimal, complete, partial)
- Python usage guide with code examples
- TypeScript usage guide with code examples
- React component integration example
- Bloodbank integration commands
- Testing instructions
- Troubleshooting common validation errors
- Versioning and compatibility guarantees
- Change log

---

## 🚀 Integration Guide for Other Teams

### For Bloodbank EM (STORY-003, STORY-004)

**You can now:**

1. **Validate Events Before Publishing**

   Python example:
   ```python
   from holyfields.generated.python.whisperlivekit.events import TranscriptionCompletedEvent
   from pydantic import ValidationError

   def bb_publish(payload: dict):
       try:
           # Validate against schema
           event = TranscriptionCompletedEvent.model_validate(payload)
           # Publish to RabbitMQ
           publish_to_rabbitmq(event.model_dump_json())
           return {"status": "success"}
       except ValidationError as e:
           return {"status": "error", "details": e.errors()}
   ```

2. **bb Command Integration**

   ```bash
   bb publish \
     --event-type whisperlivekit.transcription.completed \
     --payload '{...json payload...}'
   ```

   The payload MUST validate against:
   - Schema: `whisperlivekit/events/transcription_completed.json`
   - Event type literal: `"whisperlivekit.transcription.completed"`

### For WhisperLiveKit EM (STORY-011, STORY-012)

**You can now:**

1. **Import Schema in WhisperLiveKit**

   Add to `pyproject.toml`:
   ```toml
   dependencies = [
       "holyfields @ git+https://github.com/33GOD/holyfields.git@main"
   ]
   ```

2. **Create and Validate Events**

   ```python
   from holyfields.generated.python.whisperlivekit.events import (
       TranscriptionCompletedEvent,
       AudioMetadata,
       Format,
   )
   from datetime import datetime, timezone
   from uuid import uuid4

   # After transcription completes
   event = TranscriptionCompletedEvent(
       event_type="whisperlivekit.transcription.completed",
       timestamp=datetime.now(timezone.utc),
       session_id=session_id,  # From WebSocket connection
       source="whisperlivekit",
       target="tonny",  # Or from client request
       text=transcribed_text,
       audio_metadata=AudioMetadata(
           duration_ms=audio_duration,
           sample_rate=16000,
           channels=1,
           format=Format.pcm,
           language="en",
           confidence=whisper_confidence,
       ),
       is_final=True,
   )

   # Publish via Bloodbank
   bb_publish(event.model_dump())
   ```

3. **Integration Points**

   - Session ID: Generate UUID on WebSocket connection
   - Target: Read from client handshake or default to "tonny"
   - Audio metadata: Extract from audio buffer
   - Confidence: Get from Whisper model output

### For Tonny EM (STORY-014)

**You can now:**

1. **Subscribe to Events via Bloodbank**

   ```bash
   bb subscribe \
     --event-type whisperlivekit.transcription.completed \
     --target tonny \
     --callback http://tonny-service:8080/webhooks/transcription
   ```

2. **Validate Incoming Events**

   Python (Letta/FastAPI):
   ```python
   from fastapi import FastAPI, HTTPException
   from holyfields.generated.python.whisperlivekit.events import TranscriptionCompletedEvent
   from pydantic import ValidationError

   app = FastAPI()

   @app.post("/webhooks/transcription")
   async def handle_transcription(payload: dict):
       try:
           # Validate event
           event = TranscriptionCompletedEvent.model_validate(payload)

           # Extract transcription
           transcription = event.text
           session_id = event.session_id
           confidence = event.audio_metadata.confidence

           # Route to LLM
           response = await process_with_llm(transcription, session_id)

           return {"status": "processed", "response": response}

       except ValidationError as e:
           raise HTTPException(status_code=400, detail=e.errors())
   ```

### For Candybar EM (STORY-008)

**You can now:**

1. **Subscribe to Real-Time Events**

   TypeScript/React:
   ```typescript
   import { transcriptionCompletedEventSchema } from '@holyfields/generated/typescript/whisperlivekit/events';

   const ws = new WebSocket('ws://bloodbank/events/subscribe');

   ws.onmessage = (msg) => {
     const result = transcriptionCompletedEventSchema.safeParse(JSON.parse(msg.data));

     if (result.success) {
       // Valid event - update UI
       updateEventLog(result.data);
     } else {
       // Invalid event - log error
       console.error('Schema validation failed:', result.error);
     }
   };
   ```

2. **Display Event Fields in UI**

   All fields are strongly typed and validated:
   - `event.text` - Display transcription
   - `event.timestamp` - Format as local time
   - `event.session_id` - Group by session
   - `event.audio_metadata.confidence` - Show confidence score
   - `event.audio_metadata.duration_ms` - Show duration

### For Candystore EM (STORY-006)

**You can now:**

1. **Store Events with Validated Schema**

   ```python
   from holyfields.generated.python.whisperlivekit.events import TranscriptionCompletedEvent

   def store_event(raw_payload: dict):
       # Validate before storing
       event = TranscriptionCompletedEvent.model_validate(raw_payload)

       # Store in database
       db.execute("""
           INSERT INTO events (event_id, event_type, payload, timestamp, session_id)
           VALUES (?, ?, ?, ?, ?)
       """, (
           generate_event_id(),
           event.event_type,
           event.model_dump_json(),
           event.timestamp,
           str(event.session_id),
       ))
   ```

---

## 📋 Schema Reference Quick Guide

### Event Type

```
whisperlivekit.transcription.completed
```

### Required Fields Summary

```json
{
  "event_type": "whisperlivekit.transcription.completed",
  "timestamp": "2026-01-27T10:30:15.234Z",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "source": "whisperlivekit",
  "target": "tonny",
  "text": "Transcribed text here",
  "audio_metadata": {
    "duration_ms": 2500,
    "sample_rate": 16000,
    "channels": 1,
    "format": "pcm"
  },
  "is_final": true
}
```

### Validation Rules

- ✅ `text`: 1-10,000 characters
- ✅ `sample_rate`: 8,000-48,000 Hz
- ✅ `channels`: 1 or 2
- ✅ `format`: "pcm", "wav", "mp3", or "opus"
- ✅ `confidence`: 0.0-1.0 (optional)
- ✅ `language`: 2-letter ISO 639-1 code (optional)

---

## 🎯 Next Steps by Team

### Immediate (Week 1)

- **Bloodbank**: Integrate schema validation in `bb publish` command
- **WhisperLiveKit**: Add holyfields dependency and start publishing events

### Week 2

- **Tonny**: Implement consumer webhook with schema validation
- **Candybar**: Add real-time event display with TypeScript bindings
- **Candystore**: Add event storage with validation

### Week 3

- **All Teams**: End-to-end integration testing
- **All Teams**: Monitor event flow in Candybar

---

## 📞 Support

**HolyFields EM Responsibilities:**
- Schema updates and versioning
- Breaking change coordination
- Documentation maintenance
- Contract validation support

**Contact:**
- Schema issues: Open issue in `holyfields` repo
- Integration help: Slack #hey-ma-integration
- Emergency: Page HolyFields EM

---

## ✅ Acceptance Criteria Met

- [x] Schema file created: `whisperlivekit/events/transcription_completed.json`
- [x] Schema includes all required fields: text, timestamp, source, target, session_id, audio_metadata
- [x] Schema versioned as v1.0.0
- [x] Validation function exported for publishers (Pydantic/Zod)
- [x] Documentation includes example event payloads
- [x] Unit tests for schema validation (valid/invalid cases)
- [x] Python Pydantic model generated
- [x] TypeScript type definition generated
- [x] Both bindings importable as packages
- [x] Validation methods included in bindings
- [x] Examples of usage in both languages

---

## 🚀 Status: READY FOR INTEGRATION

All other teams are UNBLOCKED and can proceed with their stories:
- ✅ Bloodbank can implement event publishing (STORY-003, STORY-004)
- ✅ WhisperLiveKit can integrate schema (STORY-011, STORY-012)
- ✅ Tonny can implement consumer (STORY-014)
- ✅ Candybar can implement real-time display (STORY-008)
- ✅ Candystore can implement storage (STORY-006)

**Let's ship this! 🎉**

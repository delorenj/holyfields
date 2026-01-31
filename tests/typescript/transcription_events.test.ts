/**
 * Contract validation tests for WhisperLiveKit transcription events.
 *
 * Tests validate that generated Zod schemas match JSON Schema expectations
 * for the transcription.completed event.
 */

import { describe, it, expect } from 'vitest';
import { transcriptionCompletedEventSchema } from '../../generated/typescript/whisperlivekit/events/transcription_completed';

describe('TranscriptionCompletedEvent Schema', () => {
  describe('Valid Events', () => {
    it('should validate a complete valid event', () => {
      const validEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: "Hey Tonny, what's the weather like today?",
        audio_metadata: {
          duration_ms: 2500,
          sample_rate: 16000,
          channels: 1,
          bit_depth: 16,
          format: 'pcm' as const,
          language: 'en',
          confidence: 0.95,
        },
        is_final: true,
        segment_id: 'seg_001',
      };

      const result = transcriptionCompletedEventSchema.safeParse(validEvent);
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.text).toBe("Hey Tonny, what's the weather like today?");
        expect(result.data.audio_metadata.sample_rate).toBe(16000);
      }
    });

    it('should validate event with minimal required fields', () => {
      const minimalEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'Test text',
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 16000,
          channels: 1,
          format: 'pcm' as const,
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(minimalEvent);
      expect(result.success).toBe(true);
    });

    it('should validate with different audio formats', () => {
      const formats = ['pcm', 'wav', 'mp3', 'opus'] as const;

      formats.forEach((format) => {
        const event = {
          event_type: 'whisperlivekit.transcription.completed',
          timestamp: '2026-01-27T10:30:15.234Z',
          session_id: '550e8400-e29b-41d4-a716-446655440000',
          source: 'whisperlivekit',
          target: 'tonny',
          text: 'Test text',
          audio_metadata: {
            duration_ms: 1000,
            sample_rate: 16000,
            channels: 1,
            format,
          },
          is_final: true,
        };

        const result = transcriptionCompletedEventSchema.safeParse(event);
        expect(result.success).toBe(true);
      });
    });

    it('should validate with different bit depths', () => {
      const bitDepths = [8, 16, 24, 32];

      bitDepths.forEach((bit_depth) => {
        const event = {
          event_type: 'whisperlivekit.transcription.completed',
          timestamp: '2026-01-27T10:30:15.234Z',
          session_id: '550e8400-e29b-41d4-a716-446655440000',
          source: 'whisperlivekit',
          target: 'tonny',
          text: 'Test text',
          audio_metadata: {
            duration_ms: 1000,
            sample_rate: 16000,
            channels: 1,
            bit_depth,
            format: 'pcm' as const,
          },
          is_final: true,
        };

        const result = transcriptionCompletedEventSchema.safeParse(event);
        expect(result.success).toBe(true);
      });
    });
  });

  describe('Invalid Events', () => {
    it('should reject wrong event_type literal', () => {
      const invalidEvent = {
        event_type: 'wrong.event.type',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'Test text',
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 16000,
          channels: 1,
          format: 'pcm' as const,
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.issues.length).toBeGreaterThan(0);
      }
    });

    it('should reject empty text', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: '',
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 16000,
          channels: 1,
          format: 'pcm' as const,
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });

    it('should reject text exceeding max length', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'x'.repeat(10001),
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 16000,
          channels: 1,
          format: 'pcm' as const,
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });

    it('should reject negative duration_ms', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'Test text',
        audio_metadata: {
          duration_ms: -100,
          sample_rate: 16000,
          channels: 1,
          format: 'pcm' as const,
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });

    it('should reject invalid sample_rate below minimum', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'Test text',
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 4000,
          channels: 1,
          format: 'pcm' as const,
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });

    it('should reject invalid sample_rate above maximum', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'Test text',
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 96000,
          channels: 1,
          format: 'pcm' as const,
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });

    it('should reject invalid channels count', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'Test text',
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 16000,
          channels: 5,
          format: 'pcm' as const,
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });

    it('should reject invalid bit_depth', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'Test text',
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 16000,
          channels: 1,
          bit_depth: 12,
          format: 'pcm' as const,
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });

    it('should reject invalid audio format', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'Test text',
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 16000,
          channels: 1,
          format: 'flac',
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });

    it('should reject invalid language code format', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'Test text',
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 16000,
          channels: 1,
          format: 'pcm' as const,
          language: 'english',
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });

    it('should reject confidence outside valid range', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'Test text',
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 16000,
          channels: 1,
          format: 'pcm' as const,
          confidence: 1.5,
        },
        is_final: true,
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });

    it('should reject missing required fields', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        // Missing session_id, source, target, text, audio_metadata, is_final
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });

    it('should reject additional properties', () => {
      const invalidEvent = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: 'Test text',
        audio_metadata: {
          duration_ms: 1000,
          sample_rate: 16000,
          channels: 1,
          format: 'pcm' as const,
        },
        is_final: true,
        unexpected_field: 'should fail',
      };

      const result = transcriptionCompletedEventSchema.safeParse(invalidEvent);
      expect(result.success).toBe(false);
    });
  });

  describe('Example Payloads', () => {
    it('should validate first example from schema', () => {
      const example1 = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:30:15.234Z',
        session_id: '550e8400-e29b-41d4-a716-446655440000',
        source: 'whisperlivekit',
        target: 'tonny',
        text: "Hey Tonny, what's the weather like today?",
        audio_metadata: {
          duration_ms: 2500,
          sample_rate: 16000,
          channels: 1,
          bit_depth: 16,
          format: 'pcm' as const,
          language: 'en',
          confidence: 0.95,
        },
        is_final: true,
        segment_id: 'seg_001',
      };

      const result = transcriptionCompletedEventSchema.safeParse(example1);
      expect(result.success).toBe(true);
    });

    it('should validate second example from schema', () => {
      const example2 = {
        event_type: 'whisperlivekit.transcription.completed',
        timestamp: '2026-01-27T10:32:48.567Z',
        session_id: '660f9511-f30c-42e5-b827-557766551111',
        source: 'whisperlivekit',
        target: 'candybar',
        text: 'Show me the current tasks',
        audio_metadata: {
          duration_ms: 1800,
          sample_rate: 16000,
          channels: 1,
          bit_depth: 16,
          format: 'pcm' as const,
          language: 'en',
          confidence: 0.88,
        },
        is_final: true,
        segment_id: 'seg_002',
      };

      const result = transcriptionCompletedEventSchema.safeParse(example2);
      expect(result.success).toBe(true);
    });
  });
});

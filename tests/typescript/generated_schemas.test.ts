/**
 * Test generated Zod schemas for correctness
 *
 * Validates that generated schemas:
 * 1. Can parse valid data
 * 2. Reject invalid data with proper error messages
 * 3. Infer correct TypeScript types
 * 4. Compose with baseEventSchema correctly
 */

import { describe, it, expect } from 'vitest';
import {
  baseEventSchema,
  meetingCreatedEventSchema,
  meetingStartedEventSchema,
  roundCompletedEventSchema,
  commentExtractedEventSchema,
  meetingConvergedEventSchema,
  meetingCompletedEventSchema,
  meetingFailedEventSchema,
  type BaseEvent,
  type MeetingCreatedEvent,
  type MeetingCompletedEvent,
  type MeetingFailedEvent,
} from '../../generated/typescript/index.js';

describe('BaseEvent Schema', () => {
  it('should parse valid base event', () => {
    const data = {
      event_type: 'theboard.meeting.created',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
    };

    const result = baseEventSchema.parse(data);
    expect(result.event_type).toBe('theboard.meeting.created');
    expect(result.timestamp).toBe('2024-01-15T10:30:00Z');
    expect(result.meeting_id).toBe('550e8400-e29b-41d4-a716-446655440000');
  });

  it('should reject invalid timestamp format', () => {
    const data = {
      event_type: 'theboard.test',
      timestamp: 'not-a-timestamp',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
    };

    expect(() => baseEventSchema.parse(data)).toThrow();
  });

  it('should reject invalid UUID format', () => {
    const data = {
      event_type: 'theboard.test',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: 'not-a-uuid',
    };

    expect(() => baseEventSchema.parse(data)).toThrow();
  });
});

describe('MeetingCreatedEvent Schema', () => {
  it('should parse valid meeting created event', () => {
    const data: MeetingCreatedEvent = {
      event_type: 'meeting.created',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      topic: 'How can we improve AI safety?',
      strategy: 'multi_agent',
      max_rounds: 5,
      agent_count: 3,
    };

    const result = meetingCreatedEventSchema.parse(data);
    expect(result.topic).toBe('How can we improve AI safety?');
    expect(result.strategy).toBe('multi_agent');
    expect(result.max_rounds).toBe(5);
  });

  it('should reject invalid strategy enum', () => {
    const data = {
      event_type: 'meeting.created',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      topic: 'Test',
      strategy: 'invalid_strategy',
      max_rounds: 5,
    };

    expect(() => meetingCreatedEventSchema.parse(data)).toThrow();
  });

  it('should reject max_rounds below minimum', () => {
    const data = {
      event_type: 'meeting.created',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      topic: 'Test',
      strategy: 'simple',
      max_rounds: 0,
    };

    expect(() => meetingCreatedEventSchema.parse(data)).toThrow();
  });

  it('should reject max_rounds above maximum', () => {
    const data = {
      event_type: 'meeting.created',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      topic: 'Test',
      strategy: 'simple',
      max_rounds: 101,
    };

    expect(() => meetingCreatedEventSchema.parse(data)).toThrow();
  });

  it('should allow optional agent_count', () => {
    const data = {
      event_type: 'meeting.created',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      topic: 'Test',
      strategy: 'simple',
      max_rounds: 5,
    };

    const result = meetingCreatedEventSchema.parse(data);
    expect(result.agent_count).toBeUndefined();
  });

  it('should enforce event_type literal', () => {
    const data = {
      event_type: 'wrong.type',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      topic: 'Test',
      strategy: 'simple',
      max_rounds: 5,
    };

    expect(() => meetingCreatedEventSchema.parse(data)).toThrow();
  });
});

describe('CommentExtractedEvent Schema', () => {
  it('should validate category enum', () => {
    const data = {
      event_type: 'meeting.comment_extracted',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      round_num: 1,
      agent_name: 'Alice',
      comment_text: 'This is a test comment',
      category: 'recommendation',
      novelty_score: 0.85,
    };

    const result = commentExtractedEventSchema.parse(data);
    expect(result.category).toBe('recommendation');
  });

  it('should enforce novelty_score range', () => {
    const validData = {
      event_type: 'meeting.comment_extracted',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      round_num: 1,
      agent_name: 'Alice',
      comment_text: 'Test',
      category: 'idea',
      novelty_score: 0.5,
    };

    expect(() => commentExtractedEventSchema.parse(validData)).not.toThrow();

    const belowRange = { ...validData, novelty_score: -0.1 };
    expect(() => commentExtractedEventSchema.parse(belowRange)).toThrow();

    const aboveRange = { ...validData, novelty_score: 1.5 };
    expect(() => commentExtractedEventSchema.parse(aboveRange)).toThrow();
  });
});

describe('MeetingCompletedEvent Schema', () => {
  it('should parse event with nested top_comments', () => {
    const data: MeetingCompletedEvent = {
      event_type: 'meeting.completed',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      total_rounds: 5,
      total_comments: 18,
      total_cost: 0.234,
      convergence_detected: true,
      stopping_reason: 'convergence',
      top_comments: [
        {
          text: 'We should consider alignment with human values.',
          category: 'recommendation',
          novelty_score: 0.92,
          agent_name: 'Alice',
          round_num: 1,
        },
      ],
      category_distribution: { recommendation: 6, question: 5 },
      agent_participation: { Alice: 6, Bob: 6, Charlie: 6 },
    };

    const result = meetingCompletedEventSchema.parse(data);
    expect(result.top_comments).toHaveLength(1);
    expect(result.top_comments[0].agent_name).toBe('Alice');
    expect(result.top_comments[0].novelty_score).toBe(0.92);
  });

  it('should enforce top_comments max length', () => {
    const data = {
      event_type: 'meeting.completed',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      total_rounds: 5,
      total_comments: 18,
      total_cost: 0.234,
      convergence_detected: true,
      stopping_reason: 'convergence',
      top_comments: Array.from({ length: 6 }, (_, i) => ({
        text: `Comment ${i}`,
        category: 'idea',
        novelty_score: 0.8,
        agent_name: 'Alice',
        round_num: 1,
      })),
      category_distribution: {},
      agent_participation: {},
    };

    expect(() => meetingCompletedEventSchema.parse(data)).toThrow();
  });
});

describe('MeetingFailedEvent Schema', () => {
  it('should allow optional round_num and agent_name', () => {
    const data: MeetingFailedEvent = {
      event_type: 'meeting.failed',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      error_type: 'validation_error',
      error_message: 'Meeting topic cannot be empty',
    };

    const result = meetingFailedEventSchema.parse(data);
    expect(result.round_num).toBeUndefined();
    expect(result.agent_name).toBeUndefined();
  });

  it('should validate error_type enum', () => {
    const validData = {
      event_type: 'meeting.failed',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      error_type: 'agent_error',
      error_message: 'Agent timeout',
      round_num: 3,
      agent_name: 'Alice',
    };

    expect(() => meetingFailedEventSchema.parse(validData)).not.toThrow();

    const invalidData = { ...validData, error_type: 'unknown_type' };
    expect(() => meetingFailedEventSchema.parse(invalidData)).toThrow();
  });
});

describe('Schema Composition', () => {
  it('should include baseEvent fields in all event schemas', () => {
    const data = {
      event_type: 'meeting.created',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      topic: 'Test',
      strategy: 'simple',
      max_rounds: 5,
    };

    const result = meetingCreatedEventSchema.parse(data);

    // Should have base event fields
    expect(result).toHaveProperty('event_type');
    expect(result).toHaveProperty('timestamp');
    expect(result).toHaveProperty('meeting_id');

    // Should have specific event fields
    expect(result).toHaveProperty('topic');
    expect(result).toHaveProperty('strategy');
    expect(result).toHaveProperty('max_rounds');
  });
});

describe('TypeScript Type Inference', () => {
  it('should infer correct types', () => {
    const event: MeetingCreatedEvent = {
      event_type: 'meeting.created',
      timestamp: '2024-01-15T10:30:00Z',
      meeting_id: '550e8400-e29b-41d4-a716-446655440000',
      topic: 'Test',
      strategy: 'simple',
      max_rounds: 5,
    };

    // TypeScript compilation will fail if types are wrong
    expect(event.event_type).toBe('meeting.created');
    expect(event.strategy).toBe('simple');
  });
});

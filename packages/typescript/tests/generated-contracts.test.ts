import { describe, expect, it } from 'vitest';
import {
  AgentSessionStartedV1Schema,
  TheboardMeetingCreatedV1Schema,
  type AgentSessionStartedV1,
} from '../src/index.js';

const now = '2026-04-30T12:00:00Z';
const uuid = '550e8400-e29b-41d4-a716-446655440000';

describe('@33god/holyfields generated contracts', () => {
  it('validates a v3 CloudEvents contract with nested data', () => {
    const event: AgentSessionStartedV1 = {
      specversion: '1.0',
      id: uuid,
      source: 'urn:33god:agent:claude-code',
      type: 'agent.session.started',
      subject: `agent/${uuid}`,
      time: now,
      datacontenttype: 'application/json',
      correlationid: uuid,
      causationid: null,
      producer: 'claude-code',
      service: 'claude-code',
      domain: 'agent',
      schemaref: 'agent.session.started.v1',
      traceparent: '00-00000000000000000000000000000000-0000000000000000-00',
      data: {
        session_id: uuid,
        working_directory: '/home/delorenj/code/33GOD',
        started_at: now,
      },
    };

    expect(AgentSessionStartedV1Schema.parse(event).type).toBe('agent.session.started');
  });

  it('rejects an invalid v3 literal', () => {
    const result = AgentSessionStartedV1Schema.safeParse({
      type: 'agent.session.resumed',
      domain: 'agent',
      data: {
        session_id: uuid,
        working_directory: '/tmp',
        started_at: now,
      },
    });

    expect(result.success).toBe(false);
  });

  it('validates a legacy payload-shaped event', () => {
    const result = TheboardMeetingCreatedV1Schema.safeParse({
      event_type: 'theboard.meeting.created',
      payload: {
        topic: 'How should Holyfields package contracts?',
        strategy: 'sequential',
        max_rounds: 3,
        meeting_id: uuid,
      },
    });

    expect(result.success).toBe(true);
  });
});

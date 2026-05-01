from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from holyfields.generated.agent.session_started_v1 import AgentSessionStartedV1
from holyfields.generated.theboard.meeting_created_v1 import TheboardMeetingCreatedV1


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def test_v3_event_model_validates_nested_data() -> None:
    session_id = str(uuid.uuid4())
    event = AgentSessionStartedV1(
        specversion="1.0",
        id=str(uuid.uuid4()),
        source="urn:33god:agent:claude-code",
        type="agent.session.started",
        subject=f"agent/{session_id}",
        time=_now(),
        datacontenttype="application/json",
        correlationid=session_id,
        causationid=None,
        producer="claude-code",
        service="claude-code",
        domain="agent",
        schemaref="agent.session.started.v1",
        traceparent="00-00000000000000000000000000000000-0000000000000000-00",
        data={
            "session_id": session_id,
            "working_directory": "/home/delorenj/code/33GOD",
            "started_at": _now(),
        },
    )

    assert event.EVENT_TYPE == "agent.session.started"
    assert event.data.session_id == session_id


def test_v3_event_model_rejects_bad_literal() -> None:
    with pytest.raises(ValidationError):
        AgentSessionStartedV1(
            specversion="1.0",
            id=str(uuid.uuid4()),
            source="urn:33god:agent:claude-code",
            type="agent.session.resumed",
            time=_now(),
            correlationid=str(uuid.uuid4()),
            producer="claude-code",
            service="claude-code",
            domain="agent",
            data={
                "session_id": str(uuid.uuid4()),
                "working_directory": "/tmp",
                "started_at": _now(),
            },
        )


def test_legacy_payload_event_model_validates_payload() -> None:
    event = TheboardMeetingCreatedV1(
        event_id=str(uuid.uuid4()),
        event_type="theboard.meeting.created",
        timestamp=_now(),
        version="1.0.0",
        correlation_id=str(uuid.uuid4()),
        source={"host": "local", "app": "theboard", "trigger_type": "api"},
        meeting_id=str(uuid.uuid4()),
        payload={
            "topic": "How should Holyfields package contracts?",
            "strategy": "sequential",
            "max_rounds": 3,
            "meeting_id": str(uuid.uuid4()),
        },
    )

    assert event.payload.topic.startswith("How should")

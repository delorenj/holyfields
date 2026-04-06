"""Test generated agent learning models for correctness."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from holyfields.compat import (
    AgentLearningCandidateExtracted,
    AgentLearningCandidateValidated,
    AgentLearningEpisodeCreated,
    AgentLearningLessonPromoted,
    AgentLearningObservationRecorded,
    AgentLearningRetrievalApplied,
)


class TestAgentLearningObservationRecorded:
    """Validate the observation.recorded learning contract."""

    def test_valid_observation(self):
        observation = AgentLearningObservationRecorded(
            observation_id=str(uuid4()),
            agent_name="cack",
            session_key="session-123",
            decision_type="search_before_create",
            outcome="failure",
            task_tags=["ui", "component"],
            source_event_ids=[str(uuid4())],
            tool_name="exec_command",
            verification_status="failed",
            failure_mode="duplicate_abstraction",
            fix_applied="searched existing components first",
        )

        assert observation.outcome == "failure"
        assert observation.verification_status == "failed"

    def test_outcome_enum_validation(self):
        with pytest.raises(ValidationError):
            AgentLearningObservationRecorded(
                observation_id=str(uuid4()),
                agent_name="cack",
                session_key="session-123",
                decision_type="search_before_create",
                outcome="broken",
            )


class TestAgentLearningEpisodeCreated:
    """Validate the episode.created learning contract."""

    def test_valid_episode(self):
        episode = AgentLearningEpisodeCreated(
            episode_id=str(uuid4()),
            agent_name="cack",
            session_key="session-123",
            summary="Created duplicate component before searching existing kit",
            outcome="failure",
            source_observation_ids=[str(uuid4()), str(uuid4())],
            failure_mode="duplicate_abstraction",
            user_feedback_score=7,
        )

        assert episode.outcome == "failure"
        assert episode.user_feedback_score == 7

    def test_feedback_bounds(self):
        with pytest.raises(ValidationError):
            AgentLearningEpisodeCreated(
                episode_id=str(uuid4()),
                agent_name="cack",
                session_key="session-123",
                summary="Test",
                outcome="success",
                source_observation_ids=[str(uuid4())],
                user_feedback_score=11,
            )


class TestAgentLearningCandidateFlow:
    """Validate candidate extraction and promotion contracts."""

    def test_candidate_and_validation(self):
        candidate = AgentLearningCandidateExtracted(
            candidate_id=str(uuid4()),
            rule_text="Search existing components before proposing a new one.",
            supporting_episode_ids=[str(uuid4())],
            scope_skills=["prd-planner", "code-reviewer"],
            priority="high",
        )
        validation = AgentLearningCandidateValidated(
            candidate_id=candidate.candidate_id,
            eval_suite="duplicate-abstraction-v1",
            decision="promoted",
            replay_pass_rate_before=0.5,
            replay_pass_rate_after=1.0,
            regression_failures=0,
        )

        assert candidate.priority == "high"
        assert validation.decision == "promoted"

    def test_validation_decision_enum(self):
        with pytest.raises(ValidationError):
            AgentLearningCandidateValidated(
                candidate_id=str(uuid4()),
                eval_suite="duplicate-abstraction-v1",
                decision="ship_it",
            )

    def test_promoted_lesson(self):
        lesson = AgentLearningLessonPromoted(
            lesson_id=str(uuid4()),
            candidate_id=str(uuid4()),
            lesson_text="Run the narrowest verification that proves the fix.",
            scope_skills=["debugger"],
            rollout_status="active",
            ttl_days=30,
        )

        assert lesson.rollout_status == "active"
        assert lesson.ttl_days == 30


class TestAgentLearningRetrievalApplied:
    """Validate retrieval.applied contract."""

    def test_valid_retrieval(self):
        retrieval = AgentLearningRetrievalApplied(
            retrieval_id=str(uuid4()),
            agent_name="cack",
            session_key="session-123",
            lesson_ids=[str(uuid4()), str(uuid4())],
            target_skill="code-reviewer",
        )

        assert retrieval.target_skill == "code-reviewer"
        assert len(retrieval.lesson_ids) == 2

"""Bloodbank-compatible aliases for generated models.

Maps Bloodbank's existing class names to Holyfields generated models.
Use these imports when migrating Bloodbank from hand-written models.

Usage:
    from holyfields.compat import AgentError, AgentHeartbeat, ...
"""
from __future__ import annotations

# Agent domain
from holyfields.generated.python.agent.error_v1 import AgentErrorV1 as AgentError
from holyfields.generated.python.agent.feedback.requested_v1 import AgentFeedbackRequestedV1 as AgentFeedbackRequested
from holyfields.generated.python.agent.feedback.response_v1 import AgentFeedbackResponseV1 as AgentFeedbackResponse
from holyfields.generated.python.agent.heartbeat_v1 import AgentHeartbeatV1 as AgentHeartbeat
from holyfields.generated.python.agent.learning.candidate_extracted_v1 import (
    AgentLearningCandidateExtractedV1 as AgentLearningCandidateExtracted,
)
from holyfields.generated.python.agent.learning.candidate_validated_v1 import (
    AgentLearningCandidateValidatedV1 as AgentLearningCandidateValidated,
)
from holyfields.generated.python.agent.learning.episode_created_v1 import (
    AgentLearningEpisodeCreatedV1 as AgentLearningEpisodeCreated,
)
from holyfields.generated.python.agent.learning.lesson_promoted_v1 import (
    AgentLearningLessonPromotedV1 as AgentLearningLessonPromoted,
)
from holyfields.generated.python.agent.learning.lesson_rejected_v1 import (
    AgentLearningLessonRejectedV1 as AgentLearningLessonRejected,
)
from holyfields.generated.python.agent.learning.lesson_rolled_back_v1 import (
    AgentLearningLessonRolledBackV1 as AgentLearningLessonRolledBack,
)
from holyfields.generated.python.agent.learning.observation_recorded_v1 import (
    AgentLearningObservationRecordedV1 as AgentLearningObservationRecorded,
)
from holyfields.generated.python.agent.learning.retrieval_applied_v1 import (
    AgentLearningRetrievalAppliedV1 as AgentLearningRetrievalApplied,
)
from holyfields.generated.python.agent.message_received_v1 import AgentMessageReceivedV1 as AgentMessageReceived
from holyfields.generated.python.agent.message_sent_v1 import AgentMessageSentV1 as AgentMessageSent
from holyfields.generated.python.agent.session_ended_v1 import AgentSessionEndedV1 as AgentSessionEnded
from holyfields.generated.python.agent.session_started_v1 import AgentSessionStartedV1 as AgentSessionStarted
from holyfields.generated.python.agent.state_changed_v1 import AgentStateChangedV1 as AgentStateChanged
from holyfields.generated.python.agent.subagent_completed_v1 import AgentSubagentCompletedV1 as AgentSubagentCompleted
from holyfields.generated.python.agent.subagent_spawned_v1 import AgentSubagentSpawnedV1 as AgentSubagentSpawned
from holyfields.generated.python.agent.task_assigned_v1 import AgentTaskAssignedV1 as AgentTaskAssigned
from holyfields.generated.python.agent.task_completed_v1 import AgentTaskCompletedV1 as AgentTaskCompleted
from holyfields.generated.python.agent.thread.error_v1 import AgentThreadErrorV1 as AgentThreadErrorPayload
from holyfields.generated.python.agent.thread.prompt_v1 import AgentThreadPromptV1 as AgentThreadPrompt
from holyfields.generated.python.agent.thread.response_v1 import AgentThreadResponseV1 as AgentThreadResponse
from holyfields.generated.python.agent.tool_completed_v1 import AgentToolCompletedV1 as AgentToolCompleted
from holyfields.generated.python.agent.tool_invoked_v1 import AgentToolInvokedV1 as AgentToolInvoked

# TheBoard domain
from holyfields.generated.python.theboard.meeting_comment_extracted_v1 import TheboardMeetingCommentExtractedV1 as CommentExtractedPayload
from holyfields.generated.python.theboard.meeting_completed_v1 import TheboardMeetingCompletedV1 as MeetingCompletedPayload
from holyfields.generated.python.theboard.meeting_converged_v1 import TheboardMeetingConvergedV1 as MeetingConvergedPayload
from holyfields.generated.python.theboard.meeting_created_v1 import TheboardMeetingCreatedV1 as MeetingCreatedPayload
from holyfields.generated.python.theboard.meeting_failed_v1 import TheboardMeetingFailedV1 as MeetingFailedPayload
from holyfields.generated.python.theboard.meeting_round_completed_v1 import TheboardMeetingRoundCompletedV1 as RoundCompletedPayload
from holyfields.generated.python.theboard.meeting_started_v1 import TheboardMeetingStartedV1 as MeetingStartedPayload

# Session/Claude Code domain
from holyfields.generated.python.session.thread.agent.action_v1 import SessionThreadAgentActionV1 as SessionAgentToolAction
from holyfields.generated.python.session.thread.agent.thinking_v1 import SessionThreadAgentThinkingV1 as ThinkingEvent
from holyfields.generated.python.session.thread.end_v1 import SessionThreadEndV1 as SessionThreadEnd
from holyfields.generated.python.session.thread.error_v1 import SessionThreadErrorV1 as SessionThreadError
from holyfields.generated.python.session.thread.message_v1 import SessionThreadMessageV1 as SessionThreadMessage
from holyfields.generated.python.session.thread.start_v1 import SessionThreadStartV1 as SessionThreadStart

__all__ = [
    # Agent
    "AgentError", "AgentFeedbackRequested", "AgentFeedbackResponse",
    "AgentHeartbeat", "AgentMessageReceived", "AgentMessageSent",
    "AgentSessionEnded", "AgentSessionStarted", "AgentStateChanged",
    "AgentSubagentCompleted", "AgentSubagentSpawned",
    "AgentTaskAssigned", "AgentTaskCompleted",
    "AgentLearningObservationRecorded", "AgentLearningEpisodeCreated",
    "AgentLearningCandidateExtracted", "AgentLearningCandidateValidated",
    "AgentLearningLessonPromoted", "AgentLearningLessonRejected",
    "AgentLearningLessonRolledBack", "AgentLearningRetrievalApplied",
    "AgentThreadErrorPayload", "AgentThreadPrompt", "AgentThreadResponse",
    "AgentToolCompleted", "AgentToolInvoked",
    # TheBoard
    "CommentExtractedPayload", "MeetingCompletedPayload", "MeetingConvergedPayload",
    "MeetingCreatedPayload", "MeetingFailedPayload", "RoundCompletedPayload",
    "MeetingStartedPayload",
    # Session/Claude Code
    "SessionAgentToolAction", "ThinkingEvent",
    "SessionThreadEnd", "SessionThreadError", "SessionThreadMessage", "SessionThreadStart",
]

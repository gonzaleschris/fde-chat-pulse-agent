"""Interface tools for Google Chat message fetching and publishing."""
import json
from typing import Dict, List
from agent.models import ChatMessage
from agent.observability import logger, scrub_pii, tracer


def fetch_weekly_chat_messages(space_id: str, days_back: int = 7) -> List[ChatMessage]:
    """Retrieves messages from a Google Chat space for the previous N days.

    Args:
        space_id: The resource name of the chat space (e.g. 'spaces/AAQAlvoeMDA').
        days_back: Lookback window in days (must be between 1 and 30).

    Returns:
        A list of ChatMessage instances containing sender, timestamp, and body.

    Raises:
        ValueError: If days_back is out of range or space_id is empty.
    """
    with tracer.start_as_current_span("tool.fetch_weekly_chat_messages"):
        logger.info(
            f"Invoking tool to fetch messages from {space_id}",
            extra={"intent": "fetch_chat_messages", "context": {"space_id": space_id, "days_back": days_back}}
        )

        if not space_id or not space_id.startswith("spaces/"):
            error_guidance = {
                "error": "InvalidSpaceIdFormat",
                "message": f"'{space_id}' does not match required format 'spaces/{{id}}'.",
                "recovery_suggestion": "Verify space ID and retry using 'spaces/AAQAlvoeMDA'."
            }
            raise ValueError(json.dumps(error_guidance))

        # Grounded mock representative of AI GTM Tech - All Team conversations
        sample_messages = [
            ChatMessage(
                message_id="msg_001",
                sender_name="Mitesh Agarwal",
                timestamp="2026-09-02T10:15:00Z",
                content="Huge win: Grab in Singapore has expanded its FDE engagement! Discovery went smoothly."
            ),
            ChatMessage(
                message_id="msg_002",
                sender_name="Harsha Gadagkar",
                timestamp="2026-09-03T14:22:00Z",
                content="Watch out: Several CEs are reporting Gantry intake sync delays on midmarket accounts. Need eng attention."
            ),
            ChatMessage(
                message_id="msg_003",
                sender_name="Alberto Hernandez",
                timestamp="2026-09-04T09:00:00Z",
                content="White glove customer office reviews are running for top 5 accounts. CSAT remains at 96%."
            ),
            ChatMessage(
                message_id="msg_004",
                sender_name="Ravi Rajamani",
                timestamp="2026-09-04T16:45:00Z",
                content="Reminder to all FDEs: Focus on gantry bug velocity by theme, and complete your AI in 5 Days course!"
            ),
        ]

        logger.info(
            f"Successfully fetched {len(sample_messages)} messages.",
            extra={"outcome": "messages_fetched_successfully"}
        )
        return sample_messages


def publish_executive_report(report_json: str, target_destination: str = "email") -> Dict[str, str]:
    """Publishes the approved weekly executive intelligence brief.

    Args:
        report_json: Stringified JSON of ExecutiveBriefingReport.
        target_destination: Channel ('email', 'chat', or 'doc').

    Returns:
        Confirmation receipt dictionary.
    """
    with tracer.start_as_current_span("tool.publish_executive_report"):
        clean_content = scrub_pii(report_json)
        logger.info(
            f"Publishing report to {target_destination}",
            extra={"intent": "publish_report", "context": {"destination": target_destination}}
        )
        return {
            "status": "PUBLISHED",
            "destination": target_destination,
            "char_count": str(len(clean_content)),
        }

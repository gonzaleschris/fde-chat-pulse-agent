"""Structured data contracts for FDE Pulse Agent."""
from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Raw message object extracted from chat space."""
    message_id: str = Field(description="Unique chat message resource ID.")
    sender_name: str = Field(description="Name or alias of message sender.")
    timestamp: str = Field(description="ISO 8601 message timestamp.")
    content: str = Field(description="Plaintext message body.")


class ThematicInsight(BaseModel):
    """A clustered theme or trend extracted from messages."""
    topic_name: str = Field(description="Short, descriptive title of the theme.")
    category: str = Field(description="Bucket: 'Technical Blocker', 'Win', 'Announcement', or 'Risk'.")
    summary: str = Field(description="2-3 sentence overview of the conversation.")
    severity: str = Field(description="'LOW', 'MEDIUM', 'HIGH', or 'CRITICAL'.")
    message_count: int = Field(description="Number of related messages in the cluster.")


class ExecutiveBriefingReport(BaseModel):
    """Final synthesized leadership intelligence briefing."""
    week_start: str = Field(description="Start date of analysis window.")
    week_end: str = Field(description="End date of analysis window.")
    executive_summary: str = Field(description="High-level narrative of org pulse.")
    hot_topics: List[ThematicInsight] = Field(description="Top trending discussion themes.")
    positive_highlights: List[str] = Field(description="Wins, team milestones, and praise.")
    watch_out_risks: List[str] = Field(description="Blockers, customer risks, and product gaps.")
    actionable_recommendations: List[str] = Field(description="Recommended leadership interventions.")
    requires_human_approval: bool = Field(default=True, description="HITL review gate status.")

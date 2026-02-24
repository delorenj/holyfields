from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class OverworldUserProfileV1(BaseModel):
    """Emitted when a user's profile or preferences change: account updates, preference changes, premium status, or history milestones. Routing: overworld.user.profile_updated"""

    user_id: int = Field(..., description="ID of the user")
    update_type: str = Field(..., description="What aspect of the profile changed")
    account: Optional[dict | None] = Field(None, description="Account details for account-related updates")
    preferences: Optional[dict | None] = Field(None, description="User preferences when update_type is preferences_changed")
    history: Optional[dict | None] = Field(None, description="History milestone details when update_type is history_milestone")
    premium: Optional[dict | None] = Field(None, description="Premium status details for premium-related updates")

    EVENT_TYPE: str = "overworld.user.profile_updated"

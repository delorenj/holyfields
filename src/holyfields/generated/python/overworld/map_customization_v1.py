from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class OverworldMapCustomizationV1(BaseModel):
    """Emitted when a user customizes map appearance: theme selection, color overrides, marker placement/removal, or watermark changes. Routing: overworld.map.customized"""

    map_id: int = Field(..., description="ID of the map being customized")
    user_id: int = Field(..., description="ID of the user performing customization")
    customization_type: str = Field(..., description="What kind of customization was performed")
    theme: Optional[dict | None] = Field(None, description="Theme details when customization_type is theme_applied")
    colors: Optional[dict | None] = Field(None, description="Color override details when customization_type is colors_changed")
    marker: Optional[dict | None] = Field(None, description="Marker details when customization_type involves markers")
    watermark: Optional[dict | None] = Field(None, description="Watermark details when customization_type is watermark_toggled")

    EVENT_TYPE: str = "overworld.map.customized"

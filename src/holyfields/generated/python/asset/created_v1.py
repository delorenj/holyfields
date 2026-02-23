from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class AssetCreatedV1(BaseModel):
    """Event emitted when a new asset_registry row is inserted."""

    pass

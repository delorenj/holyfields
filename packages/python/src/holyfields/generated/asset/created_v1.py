from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

class AssetCreatedV1(BaseModel):
    """Event emitted when a new asset_registry row is inserted."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str
    agent_name: str = Field(..., min_length=1)
    asset_type: Literal['invite', 'font', 'coloring_page', 'mockup', 'listing_copy']
    storage_uri: str = Field(..., pattern='^(file|gs|https|s3|volume)://')
    storage_provider: str = Field(..., min_length=1)
    content_hash: str = Field(..., description='sha256 hash')
    prompt_text: str | None = None
    model_provider: str | None = None
    model_name: str | None = None
    model_params_json: dict[str, Any] | None = None
    source_event_id: str | None = None
    correlation_id: str
    lineage_parent_asset_id: str | None = None
    status: Literal['active', 'revised', 'deleted']
    created_at: str
    updated_at: str
    deleted_at: str | None = None


from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class AssetCreatedV1(BaseModel):
    """Event emitted when a new asset_registry row is inserted."""

    event_type: str
    asset_id: str
    agent_name: str
    asset_type: str
    storage_uri: str
    storage_provider: str
    content_hash: str
    prompt_text: Optional[str | None] = None
    model_provider: Optional[str | None] = None
    model_name: Optional[str | None] = None
    model_params_json: Optional[dict[str, Any]] = None
    source_event_id: Optional[str | None] = None
    correlation_id: str
    lineage_parent_asset_id: Optional[str | None] = None
    status: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str | None] = None

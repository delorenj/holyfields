from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class ArtifactLifecycleV1(BaseModel):
    """Artifact was created, updated, or deleted"""

    action: str = Field(..., description="Lifecycle action")
    kind: str = Field(..., description="Type of artifact")
    uri: str = Field(..., description="File path or URL")
    title: Optional[str | None] = Field(None, description="Artifact title")
    content: Optional[str | None] = Field(None, description="Full content if applicable")
    metadata: Optional[dict[str, Any]] = Field(None, description="Additional metadata")

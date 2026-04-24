from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class GithubPrCreatedV1(BaseModel):
    """GitHub pull request was created"""

    cache_key: str = Field(..., description="Key to retrieve PR data from cache (e.g., 'owner/repo/123')")
    repo_owner: str = Field(..., description="Repository owner")
    repo_name: str = Field(..., description="Repository name")
    pr_number: int = Field(..., description="Pull request number", ge=1)
    cache_type: Optional[Literal["redis", "memory", "file"]] = Field(None, description="Type of cache storage")

    EVENT_TYPE: str = "github.pr.created"

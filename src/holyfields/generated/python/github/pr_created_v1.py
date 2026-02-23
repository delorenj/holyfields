from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

class Payload(BaseModel):
    cache_key: str = Field(..., description="Key to retrieve PR data from cache (e.g., 'owner/repo/123')")
    cache_type: Optional[str] = Field(None, description="Type of cache storage")
    repo_owner: str = Field(..., description="Repository owner")
    repo_name: str = Field(..., description="Repository name")
    pr_number: int = Field(..., description="Pull request number")


class GithubPrCreatedV1(BaseModel):
    """GitHub pull request was created"""

    event_type: Literal["github.pr.created"] = "github.pr.created"
    payload: Payload

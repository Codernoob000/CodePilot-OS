"""Pydantic contracts for project-owned repositories."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.repository import RepositoryProvider


class RepositoryCreate(BaseModel):
    """Payload for creating a repository within a project."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    project_id: UUID
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=10_000,
    )
    provider: RepositoryProvider = RepositoryProvider.LOCAL
    remote_url: str | None = Field(
        default=None,
        max_length=2048,
    )
    default_branch: str = Field(
        default="main",
        min_length=1,
        max_length=100,
    )


class RepositoryUpdate(BaseModel):
    """Payload for partially updating mutable repository fields."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=10_000,
    )
    remote_url: str | None = Field(
        default=None,
        max_length=2048,
    )
    default_branch: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    is_connected: bool | None = None


class RepositoryResponse(BaseModel):
    """Serialized repository returned by the API."""

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )

    id: UUID
    project_id: UUID
    name: str
    description: str | None
    provider: RepositoryProvider
    remote_url: str | None = Field(
        default=None,
        max_length=2048,
    )
    default_branch: str
    is_connected: bool

    local_path: str | None = None   # ← Add this line


    created_at: datetime
    updated_at: datetime

class RepositoryStatusResponse(BaseModel):
    branch: str
    clean: bool
    modified: list[str]
    untracked: list[str]
    staged: list[str]
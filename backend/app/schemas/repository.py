"""Pydantic contracts for repository creation, updates, and responses."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class RepositoryBase(BaseModel):
    """Fields shared by repository write and read contracts."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=10_000)
    github_url: HttpUrl | None = None
    local_path: str | None = Field(default=None, min_length=1, max_length=1_024)
    default_branch: str = Field(default="main", min_length=1, max_length=255)
    language: str | None = Field(default=None, min_length=1, max_length=100)


class RepositoryCreate(RepositoryBase):
    """Payload for creating a repository."""


class RepositoryUpdate(BaseModel):
    """Partial payload for updating a repository."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=10_000)
    github_url: HttpUrl | None = None
    local_path: str | None = Field(default=None, min_length=1, max_length=1_024)
    default_branch: str | None = Field(default=None, min_length=1, max_length=255)
    language: str | None = Field(default=None, min_length=1, max_length=100)


class RepositoryResponse(RepositoryBase):
    """Serialized repository returned by the API."""

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid",
    )

    id: UUID
    created_at: datetime
    updated_at: datetime


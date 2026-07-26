"""Typed configuration loaded exclusively from environment variables."""

from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings shared by the API and future worker processes."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "CodePilot OS API"
    app_version: str = "0.1.0"
    environment: Literal["local", "test", "staging", "production"] = "local"
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"
    docs_enabled: bool = True
    cors_origins: tuple[AnyHttpUrl, ...] = Field(default=("http://localhost:3000",))

    database_url: str = "postgresql+asyncpg://codepilot:codepilot@localhost:5432/codepilot"
    redis_url: str = "redis://localhost:6379/0"
    object_storage_bucket: str | None = None
    openai_api_key: str | None = None
    github_client_id: str | None = None
    github_client_secret: str | None = None
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


@lru_cache
def get_settings() -> Settings:
    """Return one validated settings instance per process."""
    return Settings()

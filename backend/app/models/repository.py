"""Repository persistence model."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp for audit columns."""
    return datetime.now(timezone.utc)


class Repository(Base):
    """A source-code repository known to CodePilot OS."""

    __tablename__ = "repositories"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    github_url: Mapped[str | None] = mapped_column(String(2_048), nullable=True)
    local_path: Mapped[str | None] = mapped_column(String(1_024), nullable=True)
    default_branch: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="main",
    )
    language: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )


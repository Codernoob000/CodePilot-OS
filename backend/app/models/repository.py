"""Repository persistence model."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.project import Project


class RepositoryProvider(str, Enum):
    """Supported repository hosting providers."""

    LOCAL = "local"
    GITHUB = "github"


class Repository(Base):
    """A source-code repository belonging to a project."""

    __tablename__ = "repositories"
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "name",
            name="uq_project_repository_name",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    project_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    provider: Mapped[RepositoryProvider] = mapped_column(
        SQLAlchemyEnum(
            RepositoryProvider,
            name="repository_provider",
            native_enum=True,
            values_callable=lambda enum_type: [member.value for member in enum_type],
        ),
        nullable=False,
        default=RepositoryProvider.LOCAL,
    )
    remote_url: Mapped[str | None] = mapped_column(String(2_048), nullable=True)
    default_branch: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="main",
    )

    is_connected: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    local_path: Mapped[str | None] = mapped_column(
    String(500),
    nullable=True,
    )   
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="repositories",
    )


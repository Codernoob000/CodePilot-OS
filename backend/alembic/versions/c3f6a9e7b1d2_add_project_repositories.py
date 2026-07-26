"""Add project ownership and provider state to repositories.

Revision ID: c3f6a9e7b1d2
Revises: 952f424450a7
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "c3f6a9e7b1d2"
down_revision: str | Sequence[str] | None = "952f424450a7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade the legacy repositories table to the project-owned model."""
    provider_enum = postgresql.ENUM(
        "local",
        "github",
        name="repository_provider",
    )
    provider_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "repositories",
        "github_url",
        new_column_name="remote_url",
    )
    op.alter_column(
        "repositories",
        "name",
        existing_type=sa.String(length=255),
        type_=sa.String(length=100),
    )
    op.add_column(
        "repositories",
        sa.Column("project_id", sa.UUID(), nullable=False),
    )
    op.add_column(
        "repositories",
        sa.Column(
            "provider",
            provider_enum,
            nullable=False,
            server_default="local",
        ),
    )
    op.alter_column(
        "repositories",
        "default_branch",
        existing_type=sa.String(length=255),
        type_=sa.String(length=100),
        server_default="main",
    )
    op.add_column(
        "repositories",
        sa.Column(
            "is_connected",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.create_foreign_key(
        "fk_repositories_project_id_projects",
        "repositories",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_unique_constraint(
        "uq_project_repository_name",
        "repositories",
        ["project_id", "name"],
    )
    op.drop_column("repositories", "local_path")
    op.drop_column("repositories", "language")



def downgrade() -> None:
    """Restore the previous repository shape."""
    provider_enum = postgresql.ENUM(
        "local",
        "github",
        name="repository_provider",
    )

    op.add_column(
        "repositories",
        sa.Column("local_path", sa.String(length=1024), nullable=True),
    )
    op.add_column(
        "repositories",
        sa.Column("language", sa.String(length=100), nullable=True),
    )
    op.drop_constraint(
        "fk_repositories_project_id_projects",
        "repositories",
        type_="foreignkey",
    )
    op.drop_constraint(
        "uq_project_repository_name",
        "repositories",
        type_="unique",
    )
    op.drop_column("repositories", "is_connected")
    op.drop_column("repositories", "provider")
    provider_enum.drop(op.get_bind(), checkfirst=True)
    op.drop_column("repositories", "project_id")
    op.alter_column(
        "repositories",
        "default_branch",
        existing_type=sa.String(length=100),
        type_=sa.String(length=255),
        server_default=None,
    )
    op.alter_column(
        "repositories",
        "name",
        existing_type=sa.String(length=100),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "repositories",
        "remote_url",
        new_column_name="github_url",
    )

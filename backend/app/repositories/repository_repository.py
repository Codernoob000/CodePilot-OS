from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate, RepositoryUpdate


class RepositoryRepository:
    """Database access layer for Repository."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        data: RepositoryCreate,
    ) -> Repository:
        """Create and persist a new repository."""

        repository = Repository(**data.model_dump())
        self.session.add(repository)

        try:
            await self.session.commit()
            await self.session.refresh(repository)
        except Exception:
            await self.session.rollback()
            raise

        return repository

    async def get_by_id(
        self,
        repository_id: UUID,
    ) -> Repository | None:
        """Return a repository by its ID."""

        return await self.session.get(Repository, repository_id)

    async def get_all_for_project(
        self,
        project_id: UUID,
    ) -> list[Repository]:
        """Return all repositories belonging to a project."""

        result = await self.session.execute(
            select(Repository)
            .where(Repository.project_id == project_id)
            .order_by(
                Repository.created_at.desc(),
                Repository.id,
            )
        )

        return list(result.scalars().all())

    async def exists_by_name(
        self,
        project_id: UUID,
        name: str,
    ) -> bool:
        """Check whether a repository name already exists in a project."""

        stmt = select(
            exists().where(
                Repository.project_id == project_id,
                Repository.name == name,
            )
        )

        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def exists_by_name_excluding_id(
        self,
        project_id: UUID,
        repository_id: UUID,
        name: str,
    ) -> bool:
        """
        Check whether another repository with the same name exists
        in the project.
        """

        stmt = select(
            exists().where(
                Repository.project_id == project_id,
                Repository.name == name,
                Repository.id != repository_id,
            )
        )

        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def update(
        self,
        repository: Repository,
        data: RepositoryUpdate,
    ) -> Repository:
        """Update an existing repository."""

        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(repository, key, value)

        try:
            await self.session.commit()
            await self.session.refresh(repository)
        except Exception:
            await self.session.rollback()
            raise

        return repository

    async def delete(
        self,
        repository: Repository,
    ) -> None:
        """Delete a repository."""

        await self.session.delete(repository)

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
"""Business operations for repository persistence."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate, RepositoryUpdate


class RepositoryServiceError(Exception):
    """Base exception for repository business-operation failures."""


class RepositoryNotFoundError(RepositoryServiceError):
    """Raised when a requested repository does not exist."""

    def __init__(self, repository_id: UUID) -> None:
        super().__init__(f"Repository {repository_id} was not found.")
        self.repository_id = repository_id


class RepositoryService:
    """Coordinate repository business rules and persistence operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Create a service backed by an injected database session."""
        self._session = session

    async def create_repository(self, payload: RepositoryCreate) -> Repository:
        """Create, persist, and return a repository from validated input."""
        repository = Repository(**self._payload_values(payload))
        self._session.add(repository)

        try:
            await self._session.commit()
            await self._session.refresh(repository)
        except Exception:
            await self._session.rollback()
            raise

        return repository

    async def list_repositories(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Repository]:
        """Return repositories in stable creation order with bounded pagination."""
        if offset < 0:
            raise ValueError("Repository list offset cannot be negative.")
        if not 1 <= limit <= 1_000:
            raise ValueError("Repository list limit must be between 1 and 1000.")

        statement = (
            select(Repository)
            .order_by(Repository.created_at.desc(), Repository.id)
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(statement)
        return list(result.scalars().all())

    async def get_repository(self, repository_id: UUID) -> Repository:
        """Return one repository or raise a domain-level not-found error."""
        repository = await self._session.get(Repository, repository_id)
        if repository is None:
            raise RepositoryNotFoundError(repository_id)
        return repository

    async def update_repository(
        self,
        repository_id: UUID,
        payload: RepositoryUpdate,
    ) -> Repository:
        """Apply a validated partial update and return the persisted repository."""
        values = self._payload_values(payload, exclude_unset=True)
        if not values:
            raise ValueError("At least one repository field is required for an update.")

        repository = await self.get_repository(repository_id)
        for field_name, value in values.items():
            setattr(repository, field_name, value)

        try:
            await self._session.commit()
            await self._session.refresh(repository)
        except Exception:
            await self._session.rollback()
            raise

        return repository

    async def delete_repository(self, repository_id: UUID) -> None:
        """Delete a repository, raising when the requested record is absent."""
        repository = await self.get_repository(repository_id)
        await self._session.delete(repository)

        try:
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise

    @staticmethod
    def _payload_values(
        payload: RepositoryCreate | RepositoryUpdate,
        *,
        exclude_unset: bool = False,
    ) -> dict[str, object]:
        """Convert validated schema values to SQLAlchemy-compatible values."""
        values = payload.model_dump(exclude_unset=exclude_unset)
        if values.get("github_url") is not None:
            values["github_url"] = str(values["github_url"])
        return values


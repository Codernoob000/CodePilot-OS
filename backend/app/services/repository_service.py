from uuid import UUID

from app.models.repository import Repository
from app.repositories.project_repository import ProjectRepository
from app.repositories.repository_repository import RepositoryRepository
from app.schemas.repository import RepositoryCreate, RepositoryUpdate
from app.services.project_service import (
    ProjectNotFoundError,
    UnauthorizedProjectAccessError,
)

class RepositoryServiceError(Exception):
    """Base exception for repository service."""


class RepositoryNotFoundError(RepositoryServiceError):
    """Raised when a repository cannot be found."""


class DuplicateRepositoryNameError(RepositoryServiceError):
    """Raised when a duplicate repository name exists in a project."""


class UnauthorizedRepositoryAccessError(RepositoryServiceError):
    """Raised when a user accesses a repository they do not own."""


class RepositoryService:
    def __init__(
        self,
        repository: RepositoryRepository,
        project_repository: ProjectRepository,
    ) -> None:
        self.repository = repository
        self.project_repository = project_repository

    async def create_repository(
        self,
        data: RepositoryCreate,
        owner_id: UUID,
    ) -> Repository:
        """
        Create a repository inside a project.
        """

        project = await self.project_repository.get_by_id(data.project_id)

        if project is None:
            raise ProjectNotFoundError("Project not found.")

        if project.owner_id != owner_id:
            raise UnauthorizedProjectAccessError(
                "You do not own this project."
            )

        exists = await self.repository.exists_by_name(
            data.project_id,
            data.name,
        )

        if exists:
            raise DuplicateRepositoryNameError(
                "Repository name already exists in this project."
            )

        return await self.repository.create(data)

    async def list_repositories(
        self,
        project_id: UUID,
        owner_id: UUID,
    ) -> list[Repository]:
        """Return all repositories belonging to a project."""
        project = await self.project_repository.get_by_id(project_id)

        if project is None:
            raise ProjectNotFoundError("Project not found.")

        if project.owner_id != owner_id:
            raise UnauthorizedProjectAccessError(
                "You do not own this project."
            )

        return await self.repository.get_all_for_project(project_id)

    async def get_repository(
        self,
        repository_id: UUID,
        owner_id: UUID,
    ) -> Repository:
        """Return a repository if the owner has access."""
        repository = await self.repository.get_by_id(repository_id)

        if repository is None:
            raise RepositoryNotFoundError("Repository not found.")

        project = await self.project_repository.get_by_id(
            repository.project_id
        )

        if project is None:
            raise ProjectNotFoundError("Project not found.")

        if project.owner_id != owner_id:
            raise UnauthorizedProjectAccessError(
                "You do not own this project."
            )

        return repository

    async def update_repository(
        self,
        repository_id: UUID,
        owner_id: UUID,
        data: RepositoryUpdate,
    ) -> Repository:
        """Update an existing repository."""
        repository = await self.get_repository(
            repository_id,
            owner_id,
        )

        if data.name is not None:

            exists = await self.repository.exists_by_name_excluding_id(
            repository.project_id,
                repository.id,
                data.name,
            )

            if exists:
                raise DuplicateRepositoryNameError(
                    "Repository name already exists in this project."
                )

        return await self.repository.update(
            repository,
            data,
        )

    async def delete_repository(
        self,
        repository_id: UUID,
        owner_id: UUID,
    ) -> None:
        """Delete a repository."""
        repository = await self.get_repository(
            repository_id,
            owner_id,
        )

        await self.repository.delete(repository)
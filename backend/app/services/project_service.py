from uuid import UUID

from app.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectServiceError(Exception):
    pass


class ProjectNotFoundError(ProjectServiceError):
    """Raised when a project cannot be found."""


class UnauthorizedProjectAccessError(ProjectServiceError):
    """Raised when a user accesses another user's project."""

class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create_project(
        self,
        data: ProjectCreate,
        owner_id: UUID,
    ) -> Project:
        return await self.repository.create(data, owner_id)

    async def list_projects(
        self,
        owner_id: UUID,
    ) -> list[Project]:
        return await self.repository.get_all_for_user(owner_id)

    async def get_project(
        self,
        project_id: UUID,
    ) -> Project:
        project = await self.repository.get_by_id(project_id)

        if project is None:
            raise ProjectNotFoundError("Project not found.")

        return project

    async def update_project(
        self,
        project_id: UUID,
        owner_id: UUID,
        data: ProjectUpdate,
    ) -> Project:

        project = await self.get_project(project_id)

        if project.owner_id != owner_id:
            raise UnauthorizedProjectAccessError(
                "You do not own this project."
            )

        return await self.repository.update(project, data)

    async def delete_project(
        self,
        project_id: UUID,
        owner_id: UUID,
    ) -> None:

        project = await self.get_project(project_id)

        if project.owner_id != owner_id:
            raise UnauthorizedProjectAccessError(
                "You do not own this project."
            )

        await self.repository.delete(project)
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: ProjectCreate, owner_id: UUID) -> Project:
        project = Project(
            name=data.name,
            description=data.description,
            owner_id=owner_id,
        )

        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)

        return project

    async def get_by_id(self, project_id: UUID) -> Project | None:
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_all_for_user(self, owner_id: UUID) -> list[Project]:
        result = await self.db.execute(
            select(Project).where(Project.owner_id == owner_id)
        )
        return list(result.scalars().all())

    async def update(
        self,
        project: Project,
        data: ProjectUpdate,
    ) -> Project:

        if data.name is not None:
            project.name = data.name

        if data.description is not None:
            project.description = data.description

        await self.db.commit()
        await self.db.refresh(project)

        return project

    async def delete(self, project: Project) -> None:
        await self.db.delete(project)
        await self.db.commit()
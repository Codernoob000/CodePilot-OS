"""HTTP endpoints for repository resources."""

from typing import Annotated
from uuid import UUID

from app.schemas.repository import RepositoryStatusResponse
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.git.git_service import GitService
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.repositories.repository_repository import RepositoryRepository
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
    RepositoryUpdate,
)
from app.services.project_service import (
    ProjectNotFoundError,
    UnauthorizedProjectAccessError,
)
from app.services.repository_service import (
    DuplicateRepositoryNameError,
    RepositoryNotConnectedError,
    RepositoryNotFoundError,
    RepositoryService,
    RepositoryServiceError,
)
from app.git.exceptions import (
    CloneFailedError,
    RepositoryAlreadyExistsError,
)

router = APIRouter(prefix="/repositories", tags=["repositories"])

DatabaseSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
ProjectId = Annotated[
    UUID,
    Query(description="Project owning the repositories."),
]


def get_repository_service(session: DatabaseSession) -> RepositoryService:
    """Build a repository service from the request-scoped database session."""
    return RepositoryService(
        repository=RepositoryRepository(session),
        project_repository=ProjectRepository(session),
        git_service=GitService(),
    )


RepositoryServiceDependency = Annotated[
    RepositoryService,
    Depends(get_repository_service),
]


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a repository",
)

async def create_repository(
    payload: RepositoryCreate,
    service: RepositoryServiceDependency,
    current_user: CurrentUser,
) -> RepositoryResponse:
    """Create and return a repository resource."""
    try:
        repository = await service.create_repository(payload, current_user.id)
    except ProjectNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DuplicateRepositoryNameError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except UnauthorizedProjectAccessError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    return RepositoryResponse.model_validate(repository)


@router.get(
    "",
    response_model=list[RepositoryResponse],
    status_code=status.HTTP_200_OK,
    summary="List repositories",
)
async def list_repositories(
    service: RepositoryServiceDependency,
    project_id: ProjectId,
    current_user: CurrentUser,
) -> list[RepositoryResponse]:
    """Return repositories belonging to a project."""
    try:
        repositories = await service.list_repositories(project_id, current_user.id)
    except ProjectNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except UnauthorizedProjectAccessError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    return [RepositoryResponse.model_validate(repository) for repository in repositories]


@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a repository",
)
async def get_repository(
    repository_id: UUID,
    service: RepositoryServiceDependency,
    current_user: CurrentUser,
) -> RepositoryResponse:
    """Return one repository by UUID."""
    try:
        repository = await service.get_repository(repository_id, current_user.id)
    except RepositoryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ProjectNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except UnauthorizedProjectAccessError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    return RepositoryResponse.model_validate(repository)


@router.patch(
    "/{repository_id}",
    response_model=RepositoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a repository",
)
async def update_repository(
    repository_id: UUID,
    payload: RepositoryUpdate,
    service: RepositoryServiceDependency,
    current_user: CurrentUser,
) -> RepositoryResponse:
    """Apply a partial update and return the updated repository."""
    try:
        repository = await service.update_repository(
            repository_id,
            current_user.id,
            payload,
        )
    except RepositoryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ProjectNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DuplicateRepositoryNameError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except UnauthorizedProjectAccessError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    return RepositoryResponse.model_validate(repository)


@router.delete(
    "/{repository_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a repository",
)
async def delete_repository(
    repository_id: UUID,
    service: RepositoryServiceDependency,
    current_user: CurrentUser,
) -> None:
    """Delete a repository by UUID."""
    try:
        await service.delete_repository(repository_id, current_user.id)
    except RepositoryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ProjectNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except UnauthorizedProjectAccessError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc

@router.post(
    "/{repository_id}/clone",
    response_model=RepositoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Clone a repository",
)
async def clone_repository(
    repository_id: UUID,
    service: RepositoryServiceDependency,
    current_user: CurrentUser,
) -> RepositoryResponse:
    """Clone the repository to the local workspace."""
    try:
        repository = await service.clone_repository(
            repository_id,
            current_user.id,
        )
    except RepositoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ProjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except UnauthorizedProjectAccessError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    except RepositoryNotConnectedError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RepositoryAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except CloneFailedError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    except RepositoryServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return RepositoryResponse.model_validate(repository)

@router.get(
    "/{repository_id}/status",
    response_model=RepositoryStatusResponse,
)
async def get_repository_status(
    repository_id: UUID,
    current_user: User = Depends(get_current_user),
    service: RepositoryService = Depends(get_repository_service),
):
    try:
        return await service.get_repository_status(
            repository_id,
            current_user.id,
        )

    except RepositoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except RepositoryNotConnectedError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except UnauthorizedProjectAccessError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
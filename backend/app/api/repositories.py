"""HTTP endpoints for repository resources."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
    RepositoryUpdate,
)
from app.services.repository_service import (
    RepositoryNotFoundError,
    RepositoryService,
)

router = APIRouter(prefix="/repositories", tags=["repositories"])

DatabaseSession = Annotated[AsyncSession, Depends(get_db)]


def get_repository_service(session: DatabaseSession) -> RepositoryService:
    """Build a repository service from the request-scoped database session."""
    return RepositoryService(session)


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
) -> RepositoryResponse:
    """Create and return a repository resource."""
    repository = await service.create_repository(payload)
    return RepositoryResponse.model_validate(repository)


@router.get(
    "",
    response_model=list[RepositoryResponse],
    status_code=status.HTTP_200_OK,
    summary="List repositories",
)
async def list_repositories(
    service: RepositoryServiceDependency,
    offset: int = Query(default=0, ge=0, description="Number of repositories to skip."),
    limit: int = Query(default=100, ge=1, le=1_000, description="Maximum results to return."),
) -> list[RepositoryResponse]:
    """Return repositories in reverse creation order with bounded pagination."""
    repositories = await service.list_repositories(offset=offset, limit=limit)
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
) -> RepositoryResponse:
    """Return one repository by UUID."""
    try:
        repository = await service.get_repository(repository_id)
    except RepositoryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
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
) -> RepositoryResponse:
    """Apply a partial update and return the updated repository."""
    try:
        repository = await service.update_repository(repository_id, payload)
    except RepositoryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    return RepositoryResponse.model_validate(repository)


@router.delete(
    "/{repository_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a repository",
)
async def delete_repository(
    repository_id: UUID,
    service: RepositoryServiceDependency,
) -> None:
    """Delete a repository by UUID."""
    try:
        await service.delete_repository(repository_id)
    except RepositoryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


"""System health endpoint."""

from fastapi import APIRouter, Request, status

from app.schemas.health import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Return API process health",
)
async def health_check(request: Request) -> HealthResponse:
    """Report process availability; dependency checks belong to future readiness probes."""
    settings = request.app.state.settings
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
        request_id=getattr(request.state, "request_id", None),
    )

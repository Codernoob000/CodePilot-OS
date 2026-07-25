"""FastAPI application entry point for CodePilot OS."""
from app.db.base import Base
from app.db.session import engine

# Import models so SQLAlchemy registers them
from app.models.repository import Repository
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.repositories import router as repository_router
from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.logging import configure_logging, get_logger
from app.core.middleware import RequestContextMiddleware
from app.schemas.errors import ErrorResponse


def create_application(settings: Settings | None = None) -> FastAPI:
    """Create the API application without initializing business services."""
    app_settings = settings or get_settings()
    configure_logging(app_settings.log_level)
    logger = get_logger(__name__)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        logger.info("application_started", extra={"environment": app_settings.environment})

        # Create database tables during development
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield

        logger.info("application_stopped")

    app = FastAPI(
        title=app_settings.app_name,
        version=app_settings.app_version,
        description="CodePilot OS API. Business endpoints are added in later phases.",
        openapi_url=f"{app_settings.api_v1_prefix}/openapi.json",
        docs_url=f"{app_settings.api_v1_prefix}/docs" if app_settings.docs_enabled else None,
        redoc_url=None,
        lifespan=lifespan,
    )
    app.state.settings = app_settings

    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(app_settings.cors_origins),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Return a safe, consistent error envelope for unexpected failures."""
        logger.exception(
            "unhandled_exception",
            extra={"request_id": getattr(request.state, "request_id", None)},
        )
        error = ErrorResponse(
            code="internal_error",
            message="An unexpected error occurred.",
            request_id=getattr(request.state, "request_id", None),
            retryable=False,
        )
        return JSONResponse(status_code=500, content=error.model_dump())

    app.include_router(api_router, prefix=app_settings.api_v1_prefix)
    app.include_router(repository_router, prefix=app_settings.api_v1_prefix)
    return app


app = create_application()

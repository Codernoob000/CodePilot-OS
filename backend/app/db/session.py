"""Async PostgreSQL engine and FastAPI database-session dependency."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=1_800,
    pool_size=10,
    max_overflow=20,
)

SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncIterator[AsyncSession]:
    """Yield one database session per request and close it deterministically."""
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

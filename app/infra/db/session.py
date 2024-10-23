from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from app.core.configs import settings

pool_class = NullPool if settings.ENVIRONMENT == "test" else None

engine = create_async_engine(settings.database, echo=True, poolclass=pool_class)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, autocommit=False, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

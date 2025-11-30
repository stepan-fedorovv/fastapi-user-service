from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core import config

engine = create_async_engine(
    config.get_database_url(),
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def dispose_engine():
    await engine.dispose()

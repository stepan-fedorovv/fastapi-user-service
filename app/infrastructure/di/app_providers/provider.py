
from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

from app.infrastructure.db.setup import AsyncSessionLocal, engine


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return AsyncSessionLocal

    @provide(scope=Scope.APP)
    def app_engine(self) -> AsyncEngine:
        return engine

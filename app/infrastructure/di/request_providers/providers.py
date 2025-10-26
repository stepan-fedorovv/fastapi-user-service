from typing import AsyncIterator

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class RequestProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def session(self, session_factory: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

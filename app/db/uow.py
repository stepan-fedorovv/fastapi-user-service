from contextlib import asynccontextmanager
from typing import AsyncIterator, Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.setup import AsyncSessionLocal

class UnitOfWork:
    def __init__(self, session_factory: Callable[[], AsyncSession] = AsyncSessionLocal):
        self._session_factory = session_factory
        self.session: Optional[AsyncSession] = None
        self._committed = False

    @asynccontextmanager
    async def begin(self) -> AsyncIterator["UnitOfWork"]:
        async with self._session_factory() as session:
            self.session = session
            self._committed = False
            try:
                yield self
                if not self._committed:
                    await session.commit()
            except Exception:
                if session.in_transaction():
                    await session.rollback()
                raise
            finally:
                self.session = None
                self._committed = False

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UoW has no active session")
        await self.session.commit()
        self._committed = True

    async def rollback(self) -> None:
        if self.session is None:
            return
        if self.session.in_transaction():
            await self.session.rollback()

async def get_uow() -> AsyncIterator[UnitOfWork]:
    uow = UnitOfWork()
    yield uow

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.transaction import Transaction, TransactionManager


class _SATx(Transaction):
    def __init__(self, session: AsyncSession):
        self._context = session.begin()
    async def __aenter__(self):
        await self._context.__aenter__()
        return self
    async def __aexit__(self, et, e, tb):
        await self._context.__aexit__(et, e, tb)

class SATransactionManager(TransactionManager):
    def __init__(self, session: AsyncSession):
        self.session = session
    def start(self) -> Transaction:
        return _SATx(self.session)
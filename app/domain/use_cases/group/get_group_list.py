import typing

from app.domain.entities.group import Group
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.group_repository import GroupRepository


class GetGroupListUseCase:
    def __init__(self, repository: GroupRepository, transaction_manager: TransactionManager):
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self) -> typing.Sequence[Group]:
        async with self.tm.start():
            groups = await self.repository.get_all()
        return groups
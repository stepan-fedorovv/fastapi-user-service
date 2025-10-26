import typing

from app.domain.entities.permission import Permission
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.permission_repository import PermissionRepository


class GetPermissionListUseCase:
    def __init__(self, repository: PermissionRepository, transaction_manager: TransactionManager):
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self) -> typing.Sequence[Permission]:
        async with self.tm.start():
            permission = self.repository.get_all()
            return await permission

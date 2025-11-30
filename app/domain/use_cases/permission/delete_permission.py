from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.permission_repository import PermissionRepository


class DeletePermissionUseCase:
    def __init__(
        self, repository: PermissionRepository, transaction_manager: TransactionManager
    ):
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self, permission_id: int) -> None:
        async with self.tm.start():
            await self.repository.delete(
                permission_id=permission_id,
            )

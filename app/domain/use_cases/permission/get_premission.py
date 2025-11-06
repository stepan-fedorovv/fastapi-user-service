from app.domain.entities.permission import Permission
from app.domain.errors.permission_error_classes import PermissionNotFound
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.permission_repository import PermissionRepository
from app.shared.errors.enums import ErrorCode


class GetPermissionUseCase:
    def __init__(self, repository: PermissionRepository, transaction_manager: TransactionManager):
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self, permission_id: int) -> Permission:
        async with self.tm.start():
            permission = await self.repository.find_by_id(permission_id=permission_id)
            if permission is None:
                raise PermissionNotFound(
                    detail="Permission not found",
                    errors={
                        "field": 'permission_id',
                        "message": "Not found",
                        "code": ErrorCode.PERMISSION_NOT_FOUND
                    }
                )
        return permission

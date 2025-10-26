from app.domain.errors.permission_error_classes import PermissionNotFound
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.permission_repository import PermissionRepository
from app.shared.errors.enums import ErrorCode


class GetPermissionUseCase:
    def __init__(self, repository: PermissionRepository, transaction_manager: TransactionManager) -> None:
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self, code_name: str):
        async with self.tm.start():
            permission = await self.repository.find_by_code_name(
                code_name=code_name
            )
            if not permission:
                raise PermissionNotFound(
                    detail="Permission with code_name {} not found".format(code_name),
                    errors={
                        "field": "code_name",
                        "message": "Not found",
                        "code": ErrorCode.PERMISSION_NOT_FOUND
                    }
                )
        return permission

from app.domain.errors.permission_error_classes import PermissionNotFound
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.permission_repository import PermissionRepository
from app.shared.errors.enums import ErrorCode


class GetPermissionsUseCase:
    def __init__(self, repository: PermissionRepository, transaction_manager: TransactionManager) -> None:
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self, code_names: list[str]):
        async with self.tm.start():
            permissions = await self.repository.find_by_code_names(
                code_names=code_names
            )
            absence_permissions = set(code_names) - set(permission.code_name for permission in permissions)
            if absence_permissions:
                raise PermissionNotFound(
                    detail="Permission with code_names {} not found".format(','.join(absence_permissions)),
                    errors={
                        "field": "code_name",
                        "message": "Not found",
                        "code": ErrorCode.PERMISSION_NOT_FOUND
                    }
                )
        return permissions

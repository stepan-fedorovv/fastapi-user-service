import typing

from app.domain.entities.permission import Permission
from app.domain.errors.permission_error_classes import PermissionNotFound
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.permission_repository import PermissionRepository
from app.shared.errors.enums import ErrorCode


class PartialUpdatePermissionUseCase:
    def __init__(
        self, repository: PermissionRepository, transaction_manager: TransactionManager
    ):
        self.repository = repository
        self.tm = transaction_manager

    async def execute(
        self, permission_id: int, data: dict[str, typing.Any]
    ) -> Permission:
        async with self.tm.start():
            permission = await self.repository.partial_update(
                permission_id=permission_id,
                data=data,
            )
            if permission is None:
                raise PermissionNotFound(
                    detail="Permission with id {} not found".format(permission_id),
                    errors={
                        "field": "permission_id",
                        "message": "Not found",
                        "code": ErrorCode.PERMISSION_NOT_FOUND,
                    },
                )
        return permission

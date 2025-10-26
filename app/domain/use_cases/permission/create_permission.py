from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.permission import Permission
from app.domain.errors.permission_error_classes import PermissionAlreadyExists
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.permission_repository import PermissionRepository
from app.shared.errors.enums import ErrorCode


class CreatePermissionUseCase:
    def __init__(self, transaction_manager: TransactionManager, repository: PermissionRepository):
        self.tm = transaction_manager
        self.repository = repository

    async def execute(self, *, code_name: str, name: str) ->  Permission:
        async with self.tm.start():
            if await self.repository.exists_by_code_name(code_name=code_name):
                raise PermissionAlreadyExists(
                    detail="Permission with code_name {} already exists".format(code_name),
                    errors={
                        "field": "code_name",
                        "message": "Already exists",
                        "code": ErrorCode.PERMISSION_EXISTS
                    }
                )
            permission = await self.repository.create(code_name=code_name, name=name)
        return permission
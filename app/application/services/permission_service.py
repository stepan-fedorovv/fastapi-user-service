import typing

from app.application.dto.permission import PermissionDto
from app.application.factories.permission_use_case_factory import (
    PermissionUseCaseFactory,
)
from app.infrastructure.db.models import Permission


class PermissionService:
    def __init__(self, factory: PermissionUseCaseFactory):
        self.factory = factory

    async def create(self, code_name: str, name: str) -> Permission:
        return await self.factory.create_permission.execute(
            code_name=code_name,
            name=name,
        )

    async def permissions_list(self) -> typing.Sequence[Permission]:
        return await self.factory.get_permission_list.execute()

    async def get_permission(self, permission_id: int) -> Permission:
        return await self.factory.get_permission.execute(
            permission_id=permission_id,
        )

    async def delete(self, permission_id: int) -> None:
        await self.factory.get_permission.execute(permission_id=permission_id)
        return await self.factory.delete_permission.execute(
            permission_id=permission_id,
        )

    async def partial_update(self, data: PermissionDto) -> Permission:
        permission = await self.factory.partial_update_permission.execute(
            permission_id=data.id,
            data=data.model_dump(exclude_unset=True),
        )
        return permission

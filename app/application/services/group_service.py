import typing

from app.application.factories.group_use_case_factory import GroupUseCaseFactory
from app.application.factories.permission_use_case_factory import PermissionUseCaseFactory
from app.infrastructure.db.models import Group


class GroupService:
    def __init__(self, group_factory: GroupUseCaseFactory, permission_factory: PermissionUseCaseFactory) -> None:
        self.group_factory = group_factory
        self.permission_factory = permission_factory

    async def create(self, *, name: str):
        return await self.group_factory.create_group.execute(name=name)

    async def groups_list(self) -> typing.Sequence[Group]:
        return await self.group_factory.get_group_list.execute()

    async def set_permissions(self, *, group_id: int, code_name: str) -> Group:
        group = await self.group_factory.get_group.execute(
            group_id=group_id,
        )
        permission = await self.permission_factory.get_permission.execute(
            code_name=code_name,
        )
        group = await self.group_factory.set_permission.execute(
            group=group,
            permission=permission,
        )
        return group


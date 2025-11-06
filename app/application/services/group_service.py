import typing

from app.application.dto.group import GroupDto
from app.application.factories.group_use_case_factory import GroupUseCaseFactory
from app.application.factories.permission_use_case_factory import PermissionUseCaseFactory
from app.domain.contracts.group_contracts import IGroupService
from app.infrastructure.db.models import Group


class GroupService(IGroupService):
    def __init__(self, group_factory: GroupUseCaseFactory, permission_factory: PermissionUseCaseFactory) -> None:
        self.group_factory = group_factory
        self.permission_factory = permission_factory

    async def create(self, name: str):
        return await self.group_factory.create_group.execute(name=name)

    async def groups_list(self) -> typing.Sequence[Group]:
        return await self.group_factory.get_group_list.execute()

    async def retrieve(self, group_id: int) -> Group:
        group = await self.group_factory.get_group.execute(
            group_id=group_id,
        )
        return group

    async def partial_update(self, data: GroupDto) -> Group:
        group = await self.group_factory.partial_update_group.execute(
            group_id=data.id,
            payload=data.model_dump(exclude_unset=True, exclude={'permissions_code_names'}),
        )
        if data.permissions_code_names is not None:
            permissions = await self.permission_factory.get_permissions.execute(
                code_names=data.permissions_code_names,
            )
            group = await self.group_factory.set_permissions.execute(
                group=group,
                permissions=permissions,
            )
        return group
import typing
from typing import Protocol

from app.domain.entities.group import Group
from app.domain.entities.permission import Permission


class IGroupService(Protocol):

    async def create(self, name: str) -> Group:
        ...

    async def group_list(self) -> typing.Sequence[Group]:
        ...

    async def groups_list(self) -> typing.Sequence[Group]:
        ...

    async def set_permissions(self, *, group_id: int, code_name: str) -> Group:
        ...



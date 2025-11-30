import typing
from typing import Protocol

from app.application.dto.group import GroupDto
from app.domain.entities.group import Group


class IGroupService(Protocol):
    async def create(self, name: str) -> Group: ...

    async def group_list(self) -> typing.Sequence[Group]: ...

    async def groups_list(self) -> typing.Sequence[Group]: ...

    async def retrieve(self, *, group_id: int) -> Group: ...

    async def partial_update(self, *, data: GroupDto) -> Group: ...

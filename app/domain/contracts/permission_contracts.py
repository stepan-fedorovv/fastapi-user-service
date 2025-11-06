import typing
from typing import Protocol

from app.application.dto.permission import PermissionDto
from app.domain.entities.permission import Permission


class IPermissionService(Protocol):
    async def create(self, *, code_name: str, name: str) -> Permission:
        ...

    async def permissions_list(self) -> typing.Sequence[Permission]:
        ...

    async def get_permission(self, permission_id: int) -> Permission:
        ...

    async def delete(self, permission_id: int) -> None:
        ...

    async def partial_update(self, *, data: PermissionDto) -> Permission:
        ...

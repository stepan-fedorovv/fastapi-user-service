import typing
from typing import Protocol

from app.domain.entities.permission import Permission


class IPermissionService(Protocol):
    async def create(self, *, code_name: str, name: str) -> Permission:
        ...

    async def permissions_list(self) -> typing.Sequence[Permission]:
        ...
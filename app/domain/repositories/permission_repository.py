import typing
from abc import ABC, abstractmethod

from sqlalchemy import Select

from app.domain.entities.permission import Permission


class PermissionRepository(ABC):

    @abstractmethod
    async def get_all(self) -> typing.Sequence[Permission]:
        ...

    @abstractmethod
    async def create(self, *, name: str, code_name: str) -> Permission:
        ...

    @abstractmethod
    async def find_by_code_names(self, code_names: list[str]) -> Permission | None:
        ...

    @abstractmethod
    async def exists_by_code_name(self, *, code_name: str) -> bool:
        ...

    @abstractmethod
    async def delete(self, *, permission_id: int) -> None:
        ...

    @abstractmethod
    async def find_by_id(self, permission_id: int) -> Permission:
        ...

    @abstractmethod
    async def partial_update(self, permission_id: int, data: dict[str, typing.Any]) -> Permission:
        ...

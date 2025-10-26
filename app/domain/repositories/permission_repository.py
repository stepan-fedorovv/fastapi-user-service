import typing
from abc import ABC, abstractmethod

from sqlalchemy import Select

from app.domain.entities.permission import Permission


class PermissionRepository(ABC):

    @abstractmethod
    async def get_all(self) -> Select[Permission] | typing.Sequence[Permission]:
        ...
    @abstractmethod
    async def create(self, *, name: str, code_name: str) -> Permission:
        ...
    @abstractmethod
    async def find_by_code_name(self, code_name: str) -> Permission | None:
        ...
    @abstractmethod
    async def exists_by_code_name(self, *, code_name: str) -> bool:
        ...
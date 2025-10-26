import typing
from abc import abstractmethod, ABC

from sqlalchemy import Select

from app.domain.entities.group import Group


class GroupRepository(ABC):
    @abstractmethod
    async def get_all(self) -> typing.Sequence[Group]:
        ...

    @abstractmethod
    async def exists_by_name(self, *, name: str) -> bool:
        ...

    @abstractmethod
    async def find_by_id(self, *, group_id: int) -> Group:
        ...

    @abstractmethod
    async def create(self, *, name: str) -> Group:
        ...

    @abstractmethod
    async def set_permission(self, *, group: int, permission: str) -> None:
        ...

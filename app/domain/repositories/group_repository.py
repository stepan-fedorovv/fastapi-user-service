import typing
from abc import abstractmethod, ABC

from sqlalchemy import Select

from app.domain.entities.group import Group
from app.domain.entities.permission import Permission


class GroupRepository(ABC):
    @abstractmethod
    async def get_all(self) -> typing.Sequence[Group]:
        ...

    @abstractmethod
    async def find_by_name(self, *, name: str) -> Group:
        ...

    @abstractmethod
    async def find_by_id(self, *, group_id: int) -> Group:
        ...

    @abstractmethod
    async def create(self, *, name: str) -> Group:
        ...

    @abstractmethod
    async def set_permissions(self, *, group: int, permissions: list[Permission]) -> None:
        ...

    @abstractmethod
    async def patrial_update(self, *, group_id: int, data: dict[str, typing.Any]) -> Group:
        ...

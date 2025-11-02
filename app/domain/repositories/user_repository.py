import typing
from abc import ABC, abstractmethod

from app.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        ...

    @abstractmethod
    async def get_all(self) -> typing.Sequence[User]:
        ...

    @abstractmethod
    async def create(self, *, email: str, password: str, group_id: int) -> User:
        ...

    @abstractmethod
    async def find_by_email(self, *, email: str) -> User | None:
        ...

    @abstractmethod
    async def update_user(self, user_id: int, payload: dict[str, typing.Any]) -> User:
        ...

    @abstractmethod
    async def find_by_id(self, *, user_id: int) -> User | None:
        ...
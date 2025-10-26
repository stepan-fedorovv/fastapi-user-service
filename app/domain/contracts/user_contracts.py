from typing import Protocol

from fastapi_pagination import Params, Page

from app.domain.entities.user import User

class IUserService(Protocol):
    async def create(self, *, email: str, password: str, group_id: int) -> User:
        ...

    async def me(self, email: str) -> User:
        ...

    async def users_list(self) -> Page[User]:
        ...

    async def login(self, *, email: str, password: str) -> None:
        ...
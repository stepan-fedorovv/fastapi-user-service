import typing

from app.application.factories.user_use_case_factory import UserUseCaseFactory
from app.domain.contracts.user_contracts import IUserService


# TODO: Добавить возвращаемые значения

class UserService(IUserService):
    def __init__(
            self,
            factory: UserUseCaseFactory,
    ) -> None:
        self._factory = factory

    async def create(self, email: str, password: str, group_id: int):
        return await self._factory.create_user.execute(email=email, password=password, group_id=group_id)

    async def me(self, email: str):
        return await self._factory.get_user_by_email.execute(email=email)

    async def users_list(self):
        return await self._factory.get_user_list.execute()

    async def login(self, email: str, password: str):
        return await self._factory.login_user.execute(email=email, password=password)

    async def partial_update(self, user_id: int, payload: dict[str, typing.Any]):
        return await self._factory.partial_update_user.execute(user_id=user_id, payload=payload)

    async def retrieve(self, user_id: int):
        return await self._factory.get_user_by_id.execute(user_id=user_id)

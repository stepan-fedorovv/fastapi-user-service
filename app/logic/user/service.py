import typing

from app.api.routes.v1.schemas.user import UserCreateSchema, UserBaseSchema
from app.common.utils import hash_password
from app.db.uow import UnitOfWork
from app.logic.user.repository import UserRepository
from app.logic.validators.user.enums import UserValidationStates
from app.logic.validators.user.validators import UserValidatorsMixin


class UserService(UserValidatorsMixin):
    def __init__(self, uow: typing.Callable[[], UnitOfWork]) -> None:
        self.uow = uow
        super().__init__()

    async def create(self, user_create_schema: UserCreateSchema) -> UserBaseSchema:
        password = hash_password(password=user_create_schema.password)
        async with self.uow().begin() as uow:
            repository = UserRepository(uow.session)
            await self._run_validators(
                repository=repository,
                payload=user_create_schema,
                states={UserValidationStates.EMAIL_UNIQUE.value, },
            )
            user = await repository.create(
                email=user_create_schema.email,
                password=password,
                group_id=user_create_schema.group_id,
            )
            await uow.session.refresh(user, attribute_names=["group"])
            return UserBaseSchema.model_validate(user)

    async def me(self, email: str) -> UserBaseSchema:
        async with self.uow().begin() as uow:
            repository = UserRepository(uow.session)
            await self._run_validators(
                repository=repository,
                field=email,
                states={UserValidationStates.USER_EXISTS.value,},
            )
            user = await repository.find_by_email(email=email)
            return UserBaseSchema.model_validate(user)

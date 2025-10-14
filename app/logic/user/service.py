import typing

from app.api.errors.dto.user_errors import ErrorCode
from app.api.routes.v1.schemas.user import UserCreateSchema, UserResponseSchema
from app.common.errors import UserAlreadyExists
from app.common.utils import hash_password, normalize_email
from app.db.uow import UnitOfWork
from app.logic.user.repository import UserRepository
from app.logic.user.validators import UserValidatorsMixin


class UserService(UserValidatorsMixin):
    def __init__(self, uow: typing.Callable[[], UnitOfWork]) -> None:
        self.uow = uow
        super().__init__()

    async def create(self, user_create_schema: UserCreateSchema) -> UserResponseSchema:
        password = hash_password(password=user_create_schema.password)
        email = normalize_email(email=user_create_schema.email)
        async with self.uow().begin() as uow:
            repository = UserRepository(uow.session)
            await self._run_validators(repository=repository, payload=user_create_schema)
            user = await repository.create(
                email=user_create_schema.email,
                password=password,
                group_id=user_create_schema.group_id,
            )
            await uow.session.refresh(user, attribute_names=["group"])
            return UserResponseSchema.model_validate(user)

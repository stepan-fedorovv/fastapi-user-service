import typing

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.dto.user_errors import ErrorCode
from app.api.routes.v1.schemas.user import UserCreateSchema
from app.common.dto import BaseDto
from app.common.errors import UserAlreadyExists
from app.common.repository.base import BaseRepository
from app.common.utils import normalize_email
from app.logic.user.repository import UserRepository

RepoT = typing.TypeVar("RepoT", bound="BaseRepository")
PayloadT = typing.TypeVar("PayloadT", bound="BaseDto")

class Validator(typing.Protocol[RepoT, PayloadT]):
    async def __call__(self, *, repository: RepoT, payload: PayloadT) -> None: ...

class ValidatorsMixin:
    _create_validators: list[Validator] = []

    async def _run_validators(
        self,
        repository: BaseRepository,
        payload: BaseDto
    ) -> None:
        for validate in self._create_validators:
            await validate(repository=repository, payload=payload)

class UserValidatorsMixin(ValidatorsMixin):
    def __init__(self) -> None:
        self._create_validators = [
            self._validate_email_unique,
            # self._validate_group_exists,
        ]
    @staticmethod
    async def _validate_email_unique(*, repository: UserRepository, payload: UserCreateSchema) -> None:
        email = normalize_email(payload.email)
        if await repository.exists_by_email(email=payload.email):
            raise UserAlreadyExists(
                detail='User with email {} already exists'.format(email),
                errors={'field': 'email', 'message': 'Already taken', 'code': ErrorCode.EMAIL_TAKEN.value}
            )

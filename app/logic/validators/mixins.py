import typing

from app.api.errors.dto.user_errors import ErrorCode
from app.common.dto import BaseDto
from app.common.errors import DomainError
from app.common.repository.base import BaseRepository

RepoT = typing.TypeVar("RepoT", bound="BaseRepository")
PayloadT = typing.TypeVar("PayloadT", bound="BaseDto")

class Validator(typing.Protocol[RepoT, PayloadT]):
    async def __call__(self, *, repository: RepoT, payload: PayloadT) -> None: ...



class ValidatorsMixin:
    _create_validators: dict[str, dict[str, typing.Callable[..., ...]]] = {}

    async def _run_validators(
        self,
        repository: BaseRepository,
        states: set[str],
        payload: BaseDto | None = None,
        field: str | None = None,
    ) -> None:
        if field is None and payload is None:
            raise DomainError(
                detail='Can not validated',
                errors={'field': '', 'message': 'Can not validated', 'code': ErrorCode.CONFLICT.value}
            )
        for key, validate in self._create_validators.items():
            if key in states:
                await validate['method'](
                    **validate['params'](repository=repository, payload=payload, field=field)
                )
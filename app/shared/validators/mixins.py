import typing

from app.interface.errors import ErrorCode
from app.shared.dto import BaseDto
from app.interface.errors.user.errors_classes import DomainError
from app.shared.repository.base import BaseRepository

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
        validated_field: str | None = None,
    ) -> None:
        if validated_field is None and payload is None:
            raise DomainError(
                detail='Can not validated',
                errors={'field': '', 'message': 'Can not validated', 'code': ErrorCode.CONFLICT.value}
            )
        for key, validate in self._create_validators.items():
            if key in states:
                await validate['method'](
                    **validate['params'](repository=repository, payload=payload, validated_field=validated_field)
                )

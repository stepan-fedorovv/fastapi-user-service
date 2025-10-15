from app.api.errors.dto.user_errors import ErrorCode
from app.api.routes.v1.schemas.user import UserCreateSchema
from app.common.errors import UserAlreadyExists, UserDoesNotExists
from app.common.utils import normalize_email
from app.logic.user.repository import UserRepository
from app.logic.validators.mixins import ValidatorsMixin
from app.logic.validators.user.enums import UserValidationStates


class UserValidatorsMixin(
    ValidatorsMixin,
):
    def __init__(self) -> None:
        self._create_validators = {
            UserValidationStates.EMAIL_UNIQUE.value: {
                'method': self._validate_email_unique,
                'params': lambda repository, payload, field: {'repository': repository, 'payload': payload},
            },
            UserValidationStates.USER_EXISTS.value: {
                'method': self._check_email_existence,
                'params': lambda repository, payload, field: {'repository': repository, 'field': field},
            },
        }

    @staticmethod
    async def _check_email_existence(
            *,
            repository: UserRepository,
            field: str
    ) -> tuple[str, bool]:
        email = normalize_email(field)
        exists = await repository.exists_by_email(email=email)
        return email, exists

    async def _validate_email_unique(
            self,
            *,
            repository: UserRepository,
            payload: UserCreateSchema
    ) -> None:
        email, exists = await self._check_email_existence(
            field=payload.email,
            repository=repository
        )
        if exists:
            raise UserAlreadyExists(
                detail='User with email {} already exists'.format(email),
                errors={'field': 'email', 'message': 'Already taken', 'code': ErrorCode.EMAIL_TAKEN.value}
            )

    async def _validate_user_exists(
            self,
            *,
            repository: UserRepository,
            field: str | None = None,
    ) -> None:
        email, exists = self._check_email_existence(
            email=field,
            repository=repository
        )
        if not exists:
            raise UserDoesNotExists(
                detail='User with email {} does not exist'.format(email),
                errors={'field': 'email', 'message': 'Does not exists', 'code': ErrorCode.NOT_FOUND.value}
            )

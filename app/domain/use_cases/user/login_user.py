import typing

from app.domain.entities.user import User
from app.domain.errors.user_errors_classes import UserDoesNotExists, UserInvalidPassword
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.user_repository import UserRepository
from app.shared.errors.enums import ErrorCode
from app.shared.types import PositionParams


class LoginUserUseCase:
    def __init__(
        self,
        repository: UserRepository,
        verify_password: typing.Callable[PositionParams, str],
        transaction_manager: TransactionManager,
    ):
        self.repository = repository
        self.verify_password = verify_password
        self.tm = transaction_manager

    async def execute(self, email: str, password: str) -> User:
        async with self.tm.start():
            user = await self.repository.find_by_email(email=email)
            if not user:
                raise UserDoesNotExists(
                    detail=f"User with email {email} does not exist.",
                    errors={
                        "field": "email",
                        "message": "Does not exist.",
                        "code": ErrorCode.USER_NOT_FOUND,
                    },
                )
            if not self.verify_password(
                plain_password=password, hashed_password=user.password_hash
            ):
                raise UserInvalidPassword(
                    detail="User password is incorrect",
                    errors={
                        "field": "password",
                        "message": "Password is incorrect",
                        "code": ErrorCode.INVALID_PASSWORD,
                    },
                )
        return user

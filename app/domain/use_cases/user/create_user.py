import typing

from app.domain.entities.user import User
from app.domain.errors.user_errors_classes import UserAlreadyExists
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.user_repository import UserRepository
from app.shared.errors.enums import ErrorCode
from app.shared.types import PositionParams


class CreateUserUseCase:
    def __init__(
            self,
            transaction_manager: TransactionManager,
            repository: UserRepository,
            hash_password: typing.Callable[PositionParams, str],):
        self.tm = transaction_manager
        self.repository = repository
        self.hash_password = hash_password

    async def execute(self, *, email: str, password: str, group_id: int) -> User:
        async with self.tm.start():
            if await self.repository.exists_by_email(email=email):
                raise UserAlreadyExists(
                    detail='User with email "{}" already exists.'.format(email),
                    errors={
                        'field': 'email',
                        'message': 'Already exists',
                        'code': ErrorCode.EMAIL_TAKEN.value
                    },
                )
            password_hash = self.hash_password(password=password)
            user = await self.repository.create(email=email, password=password_hash, group_id=group_id)
        return user
import typing

from app.domain.entities.user import User
from app.domain.errors.user_errors_classes import UserDoesNotExists
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.user_repository import UserRepository
from app.shared.errors.enums import ErrorCode


class PartialUpdateUserUseCase:
    def __init__(self, repository: UserRepository, transaction_manager: TransactionManager):
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self, *, user_id: int, payload: dict[str, typing.Any]) -> User:
        async with self.tm.start():
            user = await self.repository.update_user(user_id=user_id, payload=payload)
            if not user:
                raise UserDoesNotExists(
                    detail="User with {} does not exist".format(user_id),
                    errors={
                        'field': 'id',
                        'message': 'Not found',
                        'code': ErrorCode.NOT_FOUND,
                    }
                )
        return user

from app.domain.errors.user_errors_classes import UserDoesNotExists
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.models import User
from app.shared.errors.enums import ErrorCode


class GetUserByEmailUseCase:
    def __init__(
        self, repository: UserRepository, transaction_manager: TransactionManager
    ):
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self, user_id: int) -> User:
        async with self.tm.start():
            user = await self.repository.find_by_id(user_id=user_id)
            if user is None:
                raise UserDoesNotExists(
                    detail='User with id "{}" does not exist'.format(user_id),
                    errors={
                        "field": "email",
                        "message": "Not found",
                        "code": ErrorCode.NOT_FOUND,
                    },
                )
        return user

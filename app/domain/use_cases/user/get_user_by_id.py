from app.domain.entities.user import User
from app.domain.errors.user_errors_classes import UserDoesNotExists
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.user_repository import UserRepository
from app.shared.errors.enums import ErrorCode


class GetUserByIdUseCase:
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
                    detail=f"The user with id {user_id} was not found.",
                    errors={
                        "field": "id",
                        "message": "The user with id {user_id} was not found",
                        "code": ErrorCode.NOT_FOUND,
                    },
                )
        return user

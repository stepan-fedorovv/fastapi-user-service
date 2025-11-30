from app.domain.entities.user import User
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.user_repository import UserRepository


class GetUserListUseCase:
    def __init__(
        self, repository: UserRepository, transaction_manager: TransactionManager
    ):
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self) -> list[User]:
        async with self.tm.start():
            users = await self.repository.get_all()
            return users

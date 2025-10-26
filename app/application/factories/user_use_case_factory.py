from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases.user.create_user import CreateUserUseCase
from app.domain.use_cases.user.get_user import GetUserUseCase
from app.domain.use_cases.user.get_user_list import GetUserListUseCase
from app.domain.use_cases.user.login_user import LoginUserUseCase
from app.infrastructure.repositories.user_repository_sa import SAUserRepository
from app.infrastructure.transactions.sqlalchemy_tm import SATransactionManager
from app.shared.utils import hash_password, verify_password


class UserUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self._repository = SAUserRepository(session)
        self._tm = SATransactionManager(session)

    @property
    def create_user(self) -> CreateUserUseCase:
        return CreateUserUseCase(
            repository=self._repository,
            transaction_manager=self._tm,
            hash_password=hash_password
        )

    @property
    def get_user(self) -> GetUserUseCase:
        return GetUserUseCase(
            repository=self._repository,
            transaction_manager=self._tm,
        )

    @property
    def login_user(self):
        return LoginUserUseCase(
            repository=self._repository,
            transaction_manager=self._tm,
            verify_password=verify_password
        )

    @property
    def get_user_list(self):
        return GetUserListUseCase(
            repository=self._repository,
            transaction_manager=self._tm,
        )
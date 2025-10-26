from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases.group.create_group import CreateGroupUseCase
from app.domain.use_cases.group.get_group import GetGroupUseCase
from app.domain.use_cases.group.get_group_list import GetGroupListUseCase
from app.domain.use_cases.group.set_group_permission import SetGroupPermissionUseCase
from app.infrastructure.repositories.group_repository_sa import SAGroupRepository
from app.infrastructure.transactions.sqlalchemy_tm import SATransactionManager


class GroupUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self._repository = SAGroupRepository(session)
        self._tm = SATransactionManager(session)

    @property
    def create_group(self):
        return CreateGroupUseCase(
            repository=self._repository,
            transaction_manager=self._tm
        )

    @property
    def get_group(self):
        return GetGroupUseCase(
            repository=self._repository,
            transaction_manager=self._tm
        )

    @property
    def get_group_list(self):
        return GetGroupListUseCase(
            repository=self._repository,
            transaction_manager=self._tm,
        )

    @property
    def set_permission(self):
        return SetGroupPermissionUseCase(
            repository=self._repository,
            transaction_manager=self._tm
        )
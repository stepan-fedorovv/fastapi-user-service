from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases.permission.create_permission import CreatePermissionUseCase
from app.domain.use_cases.permission.delete_permission import DeletePermissionUseCase
from app.domain.use_cases.permission.get_permiossion_list import (
    GetPermissionListUseCase,
)
from app.domain.use_cases.permission.get_permissions import GetPermissionsUseCase
from app.domain.use_cases.permission.get_premission import GetPermissionUseCase
from app.domain.use_cases.permission.partial_update_permission import (
    PartialUpdatePermissionUseCase,
)
from app.infrastructure.repositories.permission_repository_sa import (
    SAPermissionRepository,
)
from app.infrastructure.transactions.sqlalchemy_tm import SATransactionManager


class PermissionUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self._repository = SAPermissionRepository(session)
        self._tm = SATransactionManager(session)

    @property
    def create_permission(self):
        return CreatePermissionUseCase(
            repository=self._repository, transaction_manager=self._tm
        )

    @property
    def get_permission(self) -> GetPermissionUseCase:
        return GetPermissionUseCase(
            repository=self._repository, transaction_manager=self._tm
        )

    @property
    def get_permissions(self):
        return GetPermissionsUseCase(
            repository=self._repository, transaction_manager=self._tm
        )

    @property
    def get_permission_list(self) -> GetPermissionListUseCase:
        return GetPermissionListUseCase(
            repository=self._repository, transaction_manager=self._tm
        )

    @property
    def delete_permission(self) -> DeletePermissionUseCase:
        return DeletePermissionUseCase(
            repository=self._repository, transaction_manager=self._tm
        )

    @property
    def partial_update_permission(self) -> PartialUpdatePermissionUseCase:
        return PartialUpdatePermissionUseCase(
            repository=self._repository, transaction_manager=self._tm
        )

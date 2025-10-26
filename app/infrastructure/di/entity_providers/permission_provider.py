from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.factories.permission_use_case_factory import PermissionUseCaseFactory
from app.application.services.permission_service import PermissionService
from app.domain.contracts.permission_contracts import IPermissionService


class PermissionProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IPermissionService)
    def user_service(self, session: AsyncSession) -> IPermissionService:
        factory = PermissionUseCaseFactory(session=session)
        return PermissionService(
            factory=factory,
        )
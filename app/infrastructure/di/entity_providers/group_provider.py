from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.factories.group_use_case_factory import GroupUseCaseFactory
from app.application.factories.permission_use_case_factory import PermissionUseCaseFactory
from app.application.services.group_service import GroupService
from app.domain.contracts.group_contracts import IGroupService


class GroupProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IGroupService)
    def user_service(self, session: AsyncSession) -> IGroupService:
        permission_factory = PermissionUseCaseFactory(session=session)
        group_factory = GroupUseCaseFactory(session=session)
        return GroupService(
            group_factory=group_factory,
            permission_factory=permission_factory,
        )
from dishka import provide, Provider, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.factories.user_use_case_factory import UserUseCaseFactory
from app.application.services.user_service import UserService
from app.domain.contracts.user_contracts import IUserService
from app.infrastructure.repositories.user_repository_sa import SAUserRepository


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IUserService)
    def user_service(self, session: AsyncSession) -> IUserService:
        factory = UserUseCaseFactory(session=session)
        return UserService(
            factory=factory,
        )
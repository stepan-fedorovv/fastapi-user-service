import typing

from app.application.factories.permission_use_case_factory import PermissionUseCaseFactory
from app.domain.contracts.permission_contracts import IPermissionService
from app.infrastructure.db.models import Permission


class PermissionService(IPermissionService):
    def __init__(self, factory: PermissionUseCaseFactory):
        self.factory = factory

    async def create(self, *, code_name: str, name: str) -> Permission:
        return await self.factory.create_permission.execute(
            code_name=code_name,
            name=name,
        )

    async def permissions_list(self) -> typing.Sequence[Permission]:
        return await self.factory.get_permission_list.execute()

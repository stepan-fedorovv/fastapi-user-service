from app.domain.entities.group import Group
from app.domain.entities.permission import Permission
from app.domain.errors.permission_error_classes import PermissionAlreadySetInGroup
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.group_repository import GroupRepository


class SetGroupPermissionUseCase:
    def __init__(self,transaction_manager: TransactionManager ,repository: GroupRepository):
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self, group: Group, permission: Permission):
        async with self.tm.start():
            group = await self.repository.set_permission(group=group, permission=permission)
        return group

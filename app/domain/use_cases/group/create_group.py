from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.group import Group
from app.domain.errors.group_error_classes import GroupAlreadyExists
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.group_repository import GroupRepository
from app.shared.errors.enums import ErrorCode


class CreateGroupUseCase:
    def __init__(self, transaction_manager: TransactionManager, repository: GroupRepository):
        self.tm = transaction_manager
        self.repository = repository

    async def execute(self, *, name: str) -> Group:
        async with self.tm.start():
            if await self.repository.find_by_name(name=name):
                raise GroupAlreadyExists(
                    detail="Group with name {} already exists".format(name),
                    errors={
                        "field": "name",
                        "message": "Already exists",
                        "code": ErrorCode.GROUP_EXISTS
                    }
                )
            group = await self.repository.create(name=name)
        return group

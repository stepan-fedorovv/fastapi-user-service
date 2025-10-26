from app.domain.errors.group_error_classes import GroupDoesNotExists
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.group_repository import GroupRepository
from app.shared.errors.enums import ErrorCode


class GetGroupUseCase:
    def __init__(self, repository: GroupRepository, transaction_manager: TransactionManager):
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self, *, group_id: int):
        async with self.tm.start():
            group = await self.repository.find_by_id(group_id=group_id)
            if group is None:
                raise GroupDoesNotExists(
                    detail="Group with id {} does not exist".format(group_id),
                    errors={
                        "field": "id",
                        "message":"Not found",
                        "code": ErrorCode.GROUP_DOES_NOT_EXIST.value,

                    }
                )
        return group

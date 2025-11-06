import typing

from app.domain.entities.group import Group
from app.domain.errors.group_error_classes import GroupDoesNotExists
from app.domain.ports.transaction import TransactionManager
from app.domain.repositories.group_repository import GroupRepository
from app.shared.errors.enums import ErrorCode


class PartialUpdateGroupUseCase:
    def __init__(self, repository: GroupRepository, transaction_manager: TransactionManager) -> None:
        self.repository = repository
        self.tm = transaction_manager

    async def execute(self, group_id: int, payload: dict[str, typing.Any]) -> Group:
        async with self.tm.start():
            group = await self.repository.patrial_update(group_id=group_id, data=payload)
            if not group:
                raise GroupDoesNotExists(
                    detail="Group with id {} does not exist.".format(group_id),
                    errors={
                        'field': 'id',
                        'message': 'Not found',
                        'code': ErrorCode.GROUP_DOES_NOT_EXIST,
                    }
                )
        return group
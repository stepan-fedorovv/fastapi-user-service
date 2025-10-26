import typing

from sqlalchemy import exists, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import set_committed_value
from app.domain.repositories.group_repository import GroupRepository
from app.infrastructure.db.models import Group, Permission, group_permission_link


class SAGroupRepository(GroupRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> typing.Sequence[Group]:
        stmt = select(Group)
        groups = await self.session.execute(stmt)
        return groups.scalars().all()

    async def exists_by_name(self, *, name: str) -> bool:
        stmt = select(exists().where(Group.name == name))
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def find_by_id(self, *, group_id: int) -> Group:
        stmt = select(Group).where(Group.id == group_id).limit(1)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create(self, *, name: str) -> Group:
        group = Group(
            name=name,
        )
        self.session.add(group)
        await self.session.flush()
        set_committed_value(group, "permissions", [])
        return group

    async def set_permission(self, *, group: Group, permission: Permission) -> None:
        stmt = (
            pg_insert(group_permission_link)
            .values(group_id=group.id, permission_id=permission.id)
            .on_conflict_do_nothing(
                index_elements=(group_permission_link.c.group_id, group_permission_link.c.permission_id)
            )
        )
        await self.session.execute(stmt)
        await self.session.refresh(group)
        return group


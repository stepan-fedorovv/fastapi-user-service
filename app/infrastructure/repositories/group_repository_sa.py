import typing

from sqlalchemy import exists, select, update
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

    async def find_by_name(self, *, name: str) -> Group:
        stmt = select(Group).where(Group.name == name)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def find_by_id(self, *, group_id: int) -> Group:
        stmt = select(Group).where(Group.id == group_id).limit(1)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create(self, name: str) -> Group:
        group = Group(
            name=name,
        )
        self.session.add(group)
        await self.session.flush()
        set_committed_value(group, "permissions", [])
        return group

    async def set_permissions(self, *, group: Group, permissions: list[Permission]) -> None:
        group.permissions = permissions
        await self.session.flush()
        return group

    async def patrial_update(self, group_id: int, data: dict[str, typing.Any]) -> Group:
        stmt = (
            update(Group)
            .where(Group.id == group_id)
            .values(**data)
            .returning(Group)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

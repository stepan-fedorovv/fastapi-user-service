import typing

from sqlalchemy import select, exists, delete, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.permission_repository import PermissionRepository
from app.infrastructure.db.models import Permission


class SAPermissionRepository(PermissionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> typing.Sequence[Permission]:
        stmt = select(Permission).order_by(Permission.id)
        permissions = await self.session.execute(stmt)
        return permissions.scalars().all()

    async def create(self, *, code_name: str, name: str) -> Permission | None:
        stmt = (
            pg_insert(Permission)
            .values(code_name=code_name, name=name)
            .on_conflict_do_nothing(
                index_elements=[Permission.code_name, Permission.name]
            )
            .returning(Permission.id)
        )
        result = await self.session.execute(stmt)
        permission_id = result.scalar_one_or_none()
        permission = await self.session.get(Permission, permission_id)
        return permission

    async def find_by_code_names(self, code_names: list[str]) -> Permission | None:
        stmt = select(Permission).where(Permission.code_name.in_(code_names))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_by_id(self, permission_id: int) -> Permission | None:
        stmt = select(Permission).where(Permission.id == permission_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def exists_by_code_name(self, *, code_name: str) -> bool:
        stmt = select(exists().where(Permission.code_name == code_name))
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def delete(self, permission_id: int) -> None:
        stmt = delete(Permission).where(Permission.id == permission_id)
        await self.session.execute(stmt)

    async def partial_update(
        self, *, permission_id: int, data: dict[str, typing.Any]
    ) -> Permission | None:
        stmt = (
            update(Permission)
            .where(Permission.id == permission_id)
            .values(**data)
            .returning(Permission)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

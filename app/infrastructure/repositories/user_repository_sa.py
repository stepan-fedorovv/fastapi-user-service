import typing

from sqlalchemy import select, exists, Select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models import User
from app.domain.repositories.user_repository import UserRepository


class SAUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> typing.Sequence[User]:
        stmt = select(User).order_by(User.id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, *, email: str, password: str, group_id: int) -> User:
        user = User(
            email=email,
            password_hash=password,
            group_id=group_id,
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user, attribute_names=["group"])
        return user

    async def exists_by_email(self, *, email: str) -> bool:
        stmt = select(exists().where(User.email == email))
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def find_by_email(self, *, email: str) -> User | None:
        stmt = select(User).where(User.email == email).limit(1)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def find_by_id(self, *, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def partial_update(self, *, user_id: int, data: dict[str, typing.Any]) -> User | None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**data)
            .returning(User)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()


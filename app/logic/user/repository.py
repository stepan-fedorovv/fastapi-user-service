from sqlalchemy import select, exists

from app.common.repository.base import BaseRepository
from app.common.utils import normalize_email
from app.db.models import User


class UserRepository(BaseRepository):

    async def create(self, *, email: str, password: str, group_id: int) -> User:
        user = User(
            email=email,
            password_hash=password,
            group_id=group_id,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def exists_by_email(self, *, email: str) -> bool:
        stmt = select(exists().where(User.email == email))
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def find_by_email(self, *, email: str) -> User:
        stmt = select(User).where(User.email == email).limit(1)
        result = await self.session.execute(stmt)
        return result.scalars().first()



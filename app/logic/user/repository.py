from typing import Sequence
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repository.base import BaseRepository

class UserRepository(BaseRepository):
    ...
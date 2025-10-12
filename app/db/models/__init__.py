from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), onupdate=datetime.now())

from .user import User, UserGroup, UserGroupPermission, UserGroupPermissionAssociation  # noqa

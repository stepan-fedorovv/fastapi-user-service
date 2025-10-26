from typing import Optional, List
from datetime import datetime

import sqlalchemy
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db import Base, TimestampMixin

group_permission_link = sqlalchemy.Table(
    "user_group_permission_link",
    Base.metadata,
    sqlalchemy.Column(
        "group_id",
        sqlalchemy.ForeignKey("user_groups.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sqlalchemy.Column(
        "permission_id",
        sqlalchemy.ForeignKey("user_permission.id", ondelete="CASCADE"),  # <- фикс
        primary_key=True,
    ),
)

class Permission(Base, TimestampMixin):
    __tablename__ = "user_permission"
    __table_args__ = (
        UniqueConstraint("code_name", "name", name="uq_user_permission_code_name_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    code_name: Mapped[str] = mapped_column(unique=True, nullable=False)

    groups: Mapped[List["Group"]] = relationship(
        secondary=group_permission_link,
        back_populates="permissions",
        lazy="selectin",
    )

class Group(Base, TimestampMixin):
    __tablename__ = "user_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    permissions: Mapped[List[Permission]] = relationship(
        secondary=group_permission_link,
        back_populates="groups",
        lazy="selectin",
        cascade="save-update",
    )
    users: Mapped[List["User"]] = relationship(
        back_populates="group",
        lazy="selectin",
        cascade="save-update",
    )

class User(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    first_name: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    surname: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), index=True)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    group_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user_groups.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    group: Mapped["Group"] = relationship(
        back_populates="users",
        lazy="joined",
    )
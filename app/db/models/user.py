from datetime import datetime

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from app.db.models import Base, TimestampMixin


class UserGroupPermission(Base):
    __tablename__ = 'user_group_permission'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    code_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    group_links: Mapped[list["UserGroupPermissionAssociation"]] = relationship(
        back_populates="permission",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class UserGroupPermissionAssociation(Base):
    __tablename__ = "user_group_permission_link"
    __table_args__ = (
        UniqueConstraint("group_id", "permission_id", name="uq_group_perm"),
    )
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user_groups.id",
            ondelete="CASCADE"
        ),
        index=True,
        nullable=False
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user_group_permission.id",
            ondelete="CASCADE"
        ),
        index=True,
        nullable=False
    )
    group: Mapped["UserGroup"] = relationship(
        back_populates="permission_links",
        lazy="joined",
    )
    permission: Mapped["UserGroupPermission"] = relationship(
        back_populates="group_links",
        lazy="joined",
    )
    granted_at: Mapped[datetime] = mapped_column(
        default=datetime.now(),
        nullable=False
    )
    granted_by: Mapped[str | None] = mapped_column(
        String(100)
    )


class UserGroup(Base):
    __tablename__ = "user_groups"
    __table_args__ = (
        {"comment": "Группы пользователей"},
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    permission_links: Mapped[list["UserGroupPermissionAssociation"]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    permissions = association_proxy(
        target_collection="permission_links",
        attr="permission"
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (
        {"comment": "Пользователи системы"},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    first_name: Mapped[str | None] = mapped_column(String(100), index=True)
    surname: Mapped[str | None] = mapped_column(String(100), index=True)
    middle_name: Mapped[str | None] = mapped_column(String(100), index=True)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    group_id: Mapped[int | None] = mapped_column(
        ForeignKey("user_groups.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    group: Mapped["UserGroup"] = relationship(
        back_populates="users",
        lazy="joined",
    )

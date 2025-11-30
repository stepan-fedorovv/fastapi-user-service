from dataclasses import dataclass

from app.domain.entities.group import Group


@dataclass(frozen=True)
class User:
    id: int | None
    email: str
    password_hash: str
    group: list[Group]

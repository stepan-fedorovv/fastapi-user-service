from dataclasses import dataclass

from app.domain.entities.permission import Permission


@dataclass(frozen=True)
class Group:
    id: int
    name: str
    permissions: list[Permission]
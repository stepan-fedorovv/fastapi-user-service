from dataclasses import dataclass


@dataclass(frozen=True)
class Permission:
    id: int | None
    name: str
    code_name: str

from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id: int | None
    email: str
    password_hash: str
    group_id: int
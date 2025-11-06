from app.shared.dto import BaseDto


class PermissionDto(BaseDto):
    id: int | None = None
    name: str | None = None
    code_name: str | None = None
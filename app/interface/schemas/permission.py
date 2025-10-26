from app.shared.dto import BaseDto


class PermissionBaseSchema(BaseDto):
    id: int
    code_name: str
    name: str


class PermissionCreateSchema(BaseDto):
    name: str
    code_name: str
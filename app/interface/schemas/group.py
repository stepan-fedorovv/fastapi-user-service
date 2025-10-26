from app.interface.schemas.permission import PermissionBaseSchema
from app.shared.dto import BaseDto


class GroupBaseSchema(BaseDto):
    id: int
    name: str
    permissions: list[PermissionBaseSchema]


class GroupCreateSchema(BaseDto):
    name: str

class GroupSetPermissionSchema(BaseDto):
    code_name: str
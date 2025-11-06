import pydantic
from pydantic import field_validator

from app.interface.schemas.permission import PermissionBaseSchema
from app.shared.dto import BaseDto
from app.shared.errors.enums import ErrorCode
from app.shared.errors.error_classes import FieldRequired


class GroupBaseSchema(BaseDto):
    id: int
    name: str
    permissions: list[PermissionBaseSchema]


class GroupCreateSchema(BaseDto):
    name: str


class GroupUpdateSchema(BaseDto):
    name: str | None = None
    permissions_code_names: list[str] | None = None

    @field_validator('name', mode='before')
    @classmethod
    def name_not_none(cls, v):
        if v is None:
            raise FieldRequired(
                detail='Field cannot be empty',
                errors={
                    'field': 'name',
                    'message': 'Cannot be empty',
                    'code': ErrorCode.FIELD_REQUIRED,
                }
            )
        return v

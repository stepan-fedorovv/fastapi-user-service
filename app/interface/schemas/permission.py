from pydantic import field_validator

from app.shared.dto import BaseDto
from app.shared.errors.enums import ErrorCode
from app.shared.errors.error_classes import FieldRequired


class PermissionBaseSchema(BaseDto):
    id: int
    code_name: str
    name: str


class PermissionCreateSchema(BaseDto):
    name: str
    code_name: str

class PermissionUpdateSchema(BaseDto):
    name: str | None = None
    code_name: str | None = None
    @field_validator('code_name', mode='before')
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
from pydantic import EmailStr

from app.api.routes.v1.schemas.group import GroupResponseSchema
from app.common.dto import BaseDto


class UserCreateSchema(BaseDto):
    email: EmailStr
    password: str
    group_id: int

class UserBaseSchema(BaseDto):
    id: int
    email: str
    first_name: str | None
    surname: str | None
    middle_name: str | None
    is_active: bool
    group: GroupResponseSchema


class AuthResponseSchema(BaseDto):
    access_token: str
    refresh_token: str
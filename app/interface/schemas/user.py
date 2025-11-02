import pydantic
from pydantic import EmailStr

from app.interface.schemas.group import GroupBaseSchema
from app.shared.dto import BaseDto


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
    group: GroupBaseSchema


class LoginRequestSchema(BaseDto):
    email: EmailStr
    password: str


class AuthResponseSchema(BaseDto):
    access_token: str
    refresh_token: str


class UserUpdateSchema(BaseDto):
    first_name: str | None = None
    surname: str | None = None
    middle_name: str | None = None
    is_active: bool = pydantic.Field(default=True)

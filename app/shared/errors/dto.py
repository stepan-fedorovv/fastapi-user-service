from app.shared.dto import BaseDto
from app.shared.errors.enums import ErrorCode


class FieldError(BaseDto):
    field: str
    message: str
    code: ErrorCode


class ErrorResponseDto(BaseDto):
    status: int
    code: ErrorCode
    detail: str
    errors: list[FieldError] = []

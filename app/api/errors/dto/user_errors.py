from enum import StrEnum

from app.common.dto import BaseDto


class ErrorCode(StrEnum):
    EMAIL_TAKEN = "EMAIL_TAKEN"
    VALIDATION = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    FORBIDDEN = "FORBIDDEN"
    UNAUTHORIZED = "UNAUTHORIZED"
    CONFLICT = "CONFLICT"
    BAD_REQUEST = "BAD_REQUEST"

class FieldError(BaseDto):
    field: str
    message: str
    code: ErrorCode

class ErrorResponseDto(BaseDto):
    status: int
    code: ErrorCode
    detail: str
    errors: list[FieldError] = []


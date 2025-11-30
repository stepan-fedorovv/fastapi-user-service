import typing

from app.shared.errors.dto import ErrorResponseDto


class DomainError(Exception):
    def __init__(
        self, detail: str, errors: dict[str, typing.Any], field: str | None = None
    ) -> None:
        self.detail = detail
        self.field = field
        self.status = 400
        self.code = "BAD_REQUEST"
        self.errors = errors
        if not isinstance(self.errors, list):
            self.errors = [self.errors]

    @property
    def errors_dto(self):
        return ErrorResponseDto(
            detail=self.detail, code=self.code, status=self.status, errors=self.errors
        )

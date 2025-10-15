import typing

from app.api.errors.dto.user_errors import ErrorResponseDto


class DomainError(Exception):
    def __init__(
            self,
            detail: str,
            errors: dict[str, typing.Any],
            field: str | None = None
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
            detail=self.detail,
            code=self.code,
            status=self.status,
            errors = self.errors
        )

class UserAlreadyExists(DomainError):
    def __init__(
            self,
            **kwargs: typing.Any
    ) -> None:
        self.code = "USER_ALREADY_EXISTS"
        self.status = 409
        super().__init__(**kwargs)

class UserDoesNotExists(DomainError):
    def __init__(
            self,
            **kwargs: typing.Any
    ) -> None:
        self.code = "USER_NOT_FOUND"
        self.status = 404
        super().__init__(**kwargs)

class InvalidGroup(DomainError): ...



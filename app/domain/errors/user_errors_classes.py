import typing

from app.shared.errors.base import DomainError


class UserAlreadyExists(DomainError):
    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.code = "USER_ALREADY_EXISTS"
        self.status = 409


class UserDoesNotExists(DomainError):
    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.code = "USER_NOT_FOUND"
        self.status = 404


class UserInvalidPassword(DomainError):
    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.code = "USER_INVALID_PASSWORD"
        self.status = 400

import typing

from app.shared.errors.base import DomainError


class PermissionAlreadyExists(DomainError):
    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.code = "PERMISSION_EXISTS"
        self.status = 409


class PermissionAlreadySetInGroup(DomainError):
    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.code = "PERMISSION_ALREADY_SET"
        self.status = 409


class PermissionNotFound(DomainError):
    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.code = "PERMISSION_NOT_FOUND"
        self.status = 400

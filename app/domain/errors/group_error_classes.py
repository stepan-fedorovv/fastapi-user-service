import typing

from app.shared.errors.base import DomainError


class GroupAlreadyExists(DomainError):
    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.code = "GROUP_EXISTS"
        self.status = 409


class GroupDoesNotExists(DomainError):
    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.code = "GROUP_DOES_NOT_EXIST"
        self.status = 404

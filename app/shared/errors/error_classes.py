import typing

from app.shared.errors.base import DomainError


class FieldRequired(DomainError):
    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.code = "FIELD_REQUIRED"
        self.status = 400


class PermissionDenied(DomainError):
    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.code = "PERMISSION_DENIED"
        self.status = 403

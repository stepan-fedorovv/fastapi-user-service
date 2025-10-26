import typing

from app.db.uow import UnitOfWork


class BaseService:
    def __init__(self, uow: typing.Callable[[], UnitOfWork]) -> None:
        self.uow = uow
        super().__init__()
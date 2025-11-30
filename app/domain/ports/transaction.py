from typing import Protocol, AsyncContextManager


class Transaction(AsyncContextManager["Transaction"], Protocol): ...


class TransactionManager(Protocol):
    def start(self) -> Transaction: ...

from typing import Protocol


class BasePasswordHasher(Protocol):

    def hash(self, password: str) -> str:
        ...

    def verify(self, hash: str, password: str) -> bool:
        ...

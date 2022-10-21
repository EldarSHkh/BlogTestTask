from typing import Protocol


class PasswordHasherProto(Protocol):
    def hash(self, password: str) -> str:
        ...

    def verify(self, hash: str, password: str) -> bool:
        ...

    def check_needs_rehash(self, hash: str) -> bool:
        ...

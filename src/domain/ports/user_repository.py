from typing import Protocol

from domain.user import User


class UserRepository(Protocol):
    def save(self, user: User) -> User:
        ...

    def list_all(self) -> list[User]:
        ...

    def get_by_id(self, user_id: int) -> User | None:
        ...

    def delete(self, user_id: int) -> None:
        ...

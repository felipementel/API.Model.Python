"""Abstract repository port for user persistence."""

from typing import Protocol

from domain.user import User


class UserRepository(Protocol):
    """Protocol defining the persistence interface for User entities."""

    def save(self, user: User) -> User:
        """Persist a user and return the stored copy."""
        ...

    def list_all(self) -> list[User]:
        """Return all stored users."""
        ...

    def get_by_id(self, user_id: int) -> User | None:
        """Return a user by ID, or None if not found."""
        ...

    def delete(self, user_id: int) -> None:
        """Remove a user by ID."""
        ...

"""In-memory implementation of the UserRepository port."""

from domain.user import User


class InMemoryUserRepository:
    """Thread-unsafe in-memory store for User entities."""

    def __init__(self) -> None:
        """Initialise an empty in-memory user store."""
        self._storage: dict[int, User] = {}

    def save(self, user: User) -> User:
        """Persist a user and return the stored copy."""
        stored_user = self._clone(user)
        self._storage[user.id] = stored_user
        return self._clone(stored_user)

    def list_all(self) -> list[User]:
        """Return copies of all stored users."""
        return [self._clone(user) for user in self._storage.values()]

    def get_by_id(self, user_id: int) -> User | None:
        """Return a user by ID, or None if not found."""
        user = self._storage.get(user_id)
        if user is None:
            return None
        return self._clone(user)

    def delete(self, user_id: int) -> None:
        """Remove a user by ID (no-op if not found)."""
        self._storage.pop(user_id, None)

    @staticmethod
    def _clone(user: User) -> User:
        return User(
            id=user.id,
            nome=user.nome,
            dt_nascimento=user.dt_nascimento,
            status=user.status,
            telefones=tuple(user.telefones),
        )

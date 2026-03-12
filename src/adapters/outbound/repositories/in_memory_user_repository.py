from domain.user import User


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._storage: dict[int, User] = {}

    def save(self, user: User) -> User:
        stored_user = self._clone(user)
        self._storage[user.id] = stored_user
        return self._clone(stored_user)

    def list_all(self) -> list[User]:
        return [self._clone(user) for user in self._storage.values()]

    def get_by_id(self, user_id: int) -> User | None:
        user = self._storage.get(user_id)
        if user is None:
            return None
        return self._clone(user)

    def delete(self, user_id: int) -> None:
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

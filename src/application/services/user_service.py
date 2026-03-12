from application.commands import SaveUserCommand
from domain.errors import UserAlreadyExistsError, UserNotFoundError
from domain.ports.user_repository import UserRepository
from domain.user import User


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def create_user(self, command: SaveUserCommand) -> User:
        if self._repository.get_by_id(command.id) is not None:
            raise UserAlreadyExistsError(command.id)

        user = self._to_user(command)
        return self._repository.save(user)

    def list_users(self) -> list[User]:
        return self._repository.list_all()

    def get_user(self, user_id: int) -> User:
        user = self._repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

    def update_user(self, user_id: int, command: SaveUserCommand) -> User:
        self.get_user(user_id)
        user = self._to_user(command, user_id=user_id)
        return self._repository.save(user)

    def delete_user(self, user_id: int) -> None:
        self.get_user(user_id)
        self._repository.delete(user_id)

    @staticmethod
    def _to_user(command: SaveUserCommand, user_id: int | None = None) -> User:
        return User(
            id=user_id if user_id is not None else command.id,
            nome=command.nome,
            dt_nascimento=command.dt_nascimento,
            status=command.status,
            telefones=tuple(command.telefones),
        )

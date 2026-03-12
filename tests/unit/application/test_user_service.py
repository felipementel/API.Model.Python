from datetime import date

import pytest

from adapters.outbound.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)
from application.commands import SaveUserCommand
from application.services.user_service import UserService
from domain.errors import UserAlreadyExistsError, UserNotFoundError


def make_command(*, user_id: int = 1, nome: str = "Maria") -> SaveUserCommand:
    return SaveUserCommand(
        id=user_id,
        nome=nome,
        dt_nascimento=date(1990, 1, 10),
        status=True,
        telefones=("11999990000", "1133334444"),
    )


def test_create_user_and_list_users() -> None:
    service = UserService(repository=InMemoryUserRepository())

    created_user = service.create_user(make_command())
    users = service.list_users()

    assert created_user.id == 1
    assert created_user.nome == "Maria"
    assert len(users) == 1
    assert users[0].telefones == ("11999990000", "1133334444")


def test_create_user_with_existing_id_raises_error() -> None:
    service = UserService(repository=InMemoryUserRepository())
    command = make_command()
    service.create_user(command)

    with pytest.raises(UserAlreadyExistsError):
        service.create_user(command)


def test_update_user_replaces_existing_data() -> None:
    service = UserService(repository=InMemoryUserRepository())
    service.create_user(make_command())

    updated_user = service.update_user(
        1,
        SaveUserCommand(
            id=99,
            nome="Ana",
            dt_nascimento=date(1988, 5, 20),
            status=False,
            telefones=("11888887777",),
        ),
    )

    assert updated_user.id == 1
    assert updated_user.nome == "Ana"
    assert updated_user.status is False
    assert updated_user.telefones == ("11888887777",)


def test_delete_unknown_user_raises_error() -> None:
    service = UserService(repository=InMemoryUserRepository())

    with pytest.raises(UserNotFoundError):
        service.delete_user(999)

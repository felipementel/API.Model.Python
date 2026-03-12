from fastapi.testclient import TestClient

from adapters.outbound.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)
from application.services.user_service import UserService
from main import create_app


def test_health_endpoints_report_application_status() -> None:
    app = create_app(user_service=UserService(repository=InMemoryUserRepository()))
    client = TestClient(app)

    live_response = client.get("/health/live")
    ready_response = client.get("/health/ready")

    assert live_response.status_code == 200
    assert live_response.json() == {"status": "alive"}
    assert ready_response.status_code == 200
    assert ready_response.json() == {
        "status": "ready",
        "persistence": "in-memory",
    }


def test_readiness_returns_503_when_service_is_not_available() -> None:
    app = create_app(user_service=UserService(repository=InMemoryUserRepository()))
    app.state.user_service = None
    client = TestClient(app)

    ready_response = client.get("/health/ready")

    assert ready_response.status_code == 503
    assert ready_response.json() == {"detail": "User service unavailable."}


def test_users_api_crud_flow() -> None:
    app = create_app(user_service=UserService(repository=InMemoryUserRepository()))
    client = TestClient(app)

    create_response = client.post(
        "/usuarios",
        json={
            "id": 1,
            "nome": "Carlos",
            "dtNascimento": "1992-03-14",
            "status": True,
            "telefones": ["11911112222", "1122223333"],
        },
    )

    assert create_response.status_code == 201
    assert create_response.json() == {
        "id": 1,
        "nome": "Carlos",
        "dtNascimento": "1992-03-14",
        "status": True,
        "telefones": ["11911112222", "1122223333"],
    }

    list_response = client.get("/usuarios")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get("/usuarios/1")
    assert get_response.status_code == 200
    assert get_response.json()["nome"] == "Carlos"

    update_response = client.put(
        "/usuarios/1",
        json={
            "id": 200,
            "nome": "Carlos Silva",
            "dtNascimento": "1992-03-14",
            "status": False,
            "telefones": ["11900001111"],
        },
    )

    assert update_response.status_code == 200
    assert update_response.json() == {
        "id": 1,
        "nome": "Carlos Silva",
        "dtNascimento": "1992-03-14",
        "status": False,
        "telefones": ["11900001111"],
    }

    delete_response = client.delete("/usuarios/1")
    assert delete_response.status_code == 204

    missing_response = client.get("/usuarios/1")
    assert missing_response.status_code == 404


def test_users_api_returns_409_for_duplicate_id() -> None:
    app = create_app(user_service=UserService(repository=InMemoryUserRepository()))
    client = TestClient(app)

    payload = {
        "id": 1,
        "nome": "Patricia",
        "dtNascimento": "1995-08-10",
        "status": True,
        "telefones": ["11977776666"],
    }

    first_response = client.post("/usuarios", json=payload)
    duplicate_response = client.post("/usuarios", json=payload)

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409


def test_users_api_returns_404_for_unknown_user() -> None:
    app = create_app(user_service=UserService(repository=InMemoryUserRepository()))
    client = TestClient(app)

    get_response = client.get("/usuarios/999")
    update_response = client.put(
        "/usuarios/999",
        json={
            "id": 999,
            "nome": "Inexistente",
            "dtNascimento": "2000-01-01",
            "status": False,
            "telefones": [],
        },
    )
    delete_response = client.delete("/usuarios/999")

    assert get_response.status_code == 404
    assert update_response.status_code == 404
    assert delete_response.status_code == 404

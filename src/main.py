from fastapi import FastAPI
import uvicorn

from adapters.inbound.http.routes.health import router as health_router
from adapters.inbound.http.routes.users import router as users_router
from adapters.outbound.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)
from application.services.user_service import UserService


def build_user_service() -> UserService:
    repository = InMemoryUserRepository()
    return UserService(repository=repository)


def create_app(user_service: UserService | None = None) -> FastAPI:
    app = FastAPI(
        title="Usuarios API",
        version="0.1.0",
        description="CRUD de usuarios com persistencia em memoria.",
    )
    app.state.user_service = user_service or build_user_service()
    app.include_router(health_router)
    app.include_router(users_router)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

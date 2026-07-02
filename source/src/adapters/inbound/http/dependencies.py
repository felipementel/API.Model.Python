"""HTTP dependency injectors for FastAPI route handlers."""

from fastapi import Request

from application.services.user_service import UserService


def get_user_service(request: Request) -> UserService:
    """Retrieve the UserService from the application state."""
    return request.app.state.user_service

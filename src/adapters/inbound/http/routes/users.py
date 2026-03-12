from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from adapters.inbound.http.dependencies import get_user_service
from adapters.inbound.http.schemas import UserRequest, UserResponse
from application.services.user_service import UserService
from domain.errors import UserAlreadyExistsError, UserNotFoundError

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserRequest, user_service: UserServiceDependency) -> UserResponse:
    try:
        user = user_service.create_user(payload.to_command())
    except UserAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error

    return UserResponse.from_domain(user)


@router.get("", response_model=list[UserResponse])
def list_users(user_service: UserServiceDependency) -> list[UserResponse]:
    users = user_service.list_users()
    return [UserResponse.from_domain(user) for user in users]


@router.get("/{usuario_id}", response_model=UserResponse)
def get_user(usuario_id: int, user_service: UserServiceDependency) -> UserResponse:
    try:
        user = user_service.get_user(usuario_id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    return UserResponse.from_domain(user)


@router.put("/{usuario_id}", response_model=UserResponse)
def update_user(
    usuario_id: int,
    payload: UserRequest,
    user_service: UserServiceDependency,
) -> UserResponse:
    try:
        user = user_service.update_user(usuario_id, payload.to_command())
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    return UserResponse.from_domain(user)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(usuario_id: int, user_service: UserServiceDependency) -> Response:
    try:
        user_service.delete_user(usuario_id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    return Response(status_code=status.HTTP_204_NO_CONTENT)

from fastapi import APIRouter, Response, Request

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    UserEmailAlreadyExistsHTTPException,
    UserAlreadyExistsException,
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    NoPasswordHTTPException,
    NoPasswordException,
    UserNotAuthenticatedException,
    UserNotAuthenticatedHTTPException,
)

from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
):
    try:
        await AuthService(db).register_user(data)
    except NoPasswordException:
        raise NoPasswordHTTPException
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    try:
        access_token = await AuthService(db).login_user(data, response)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    return {"access_token": access_token}


@router.get("/me", summary="👨‍💻 Мои данные")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    return await AuthService(db).get_me(user_id)


@router.post("/logout")
async def logout(response: Response, request: Request):
    try:
        await AuthService().logout(response, request)
    except UserNotAuthenticatedException:
        raise UserNotAuthenticatedHTTPException
    return {"status": "OK"}

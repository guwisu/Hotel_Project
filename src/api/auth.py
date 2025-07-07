from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserEmailAlreadyExistsHTTPException, UserAlreadyExistsException, EmailNotRegisteredException, \
    EmailNotRegisteredHTTPException, IncorrectPasswordException, IncorrectPasswordHTTPException

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


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    return await AuthService(db).get_me(user_id)


@router.post("/logout")
async def logout(response: Response):
    await AuthService().logout(response)
    return {"status": "OK"}

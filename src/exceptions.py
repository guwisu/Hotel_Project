from fastapi import HTTPException
from datetime import date


class SnapBookException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(SnapBookException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class AllRoomsAreBookedException(SnapBookException):
    detail = "Не осталось свободных номеров"


class IncorrectTokenException(SnapBookException):
    detail = "Некорректный токен"


class IncorrectPasswordException(SnapBookException):
    detail = "Пароль неверный"


class ObjectAlreadyExistsException(SnapBookException):
    detail = "Похожий объект уже существует"


class UserEmailAlreadyExistsException(SnapBookException):
    detail = "Пользователь с такой почтой уже существует"


class UserAlreadyExistsException(SnapBookException):
    detail = "Пользователь уже существует"


def check_date_to_after_date_from(date_from:date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class SnapBookHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(SnapBookHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(SnapBookHTTPException):
    status_code = 404
    detail = "Номер не найден"


class AllRoomsAreBookedHTTPException(SnapBookHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class UserEmailAlreadyExistsHTTPException(SnapBookHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class IncorrectTokenHTTPException(SnapBookException):
    detail = "Некорректный токен"


class IncorrectPasswordHTTPException(SnapBookException):
    status_code = 401
    detail = "Пароль неверный"



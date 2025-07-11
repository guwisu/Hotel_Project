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

class FacilityNotFoundException(ObjectNotFoundException):
    detail = "Удобство не найдено"

class AllRoomsAreBookedException(SnapBookException):
    detail = "Не осталось свободных номеров"


class IncorrectTokenException(SnapBookException):
    detail = "Некорректный токен"

class NoAccessTokenException(SnapBookException):
    detail = "Вы не предоставили токен доступа"


class IncorrectPasswordException(SnapBookException):
    detail = "Пароль неверный"

class NoPasswordException(SnapBookException):
    detail = "Пароль не указан"

class UserNotAuthenticatedException(SnapBookException):
    detail = "Вы не вошли в аккаунт"

class ObjectAlreadyExistsException(SnapBookException):
    detail = "Похожий объект уже существует"

class HotelAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Похожий отель уже существует"

class FacilityAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Похожее удобство уже существует"

class HotelEmptyDataException(SnapBookException):
    detail = "Вы не ввели название или локацию"

class RoomEmptyDataException(SnapBookException):
    detail = "Вы не ввели название или описание"

class FacilityEmptyDataException(SnapBookException):
    detail = "Вы не ввели название удобства"

class HotelAndRoomNotRelatedException(SnapBookException):
    detail = "Этот отель и номер не связаны"

class UserEmailAlreadyExistsException(SnapBookException):
    detail = "Пользователь с такой почтой уже существует"

class UserAlreadyExistsException(SnapBookException):
    detail = "Пользователь уже существует"

class EmailNotRegisteredException(SnapBookException):
    detail = "Пользователь с таким email не зарегистрирован"

def check_date_to_after_date_from(date_from:date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class SnapBookHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class ObjectNotFoundHTTPException(SnapBookHTTPException):
    status_code = 404
    detail = "Объект не найден"

class HotelNotFoundHTTPException(SnapBookHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(SnapBookHTTPException):
    status_code = 404
    detail = "Номер не найден"

class FacilityNotFoundHTTPException(SnapBookHTTPException):
    status_code = 404
    detail = "Удобство не найдено"


class AllRoomsAreBookedHTTPException(SnapBookHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class UserEmailAlreadyExistsHTTPException(SnapBookHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"

class HotelAlreadyExistsHTTPException(SnapBookHTTPException):
    status_code =409
    detail = "Похожий отель уже существует"

class FacilityAlreadyExistsHTTPException(SnapBookHTTPException):
    status_code = 409
    detail = "Похожее удобство уже существует"

class HotelEmptyDataHTTPException(SnapBookHTTPException):
    status_code = 401
    detail = "Вы не ввели название или локацию"

class RoomEmptyDataHTTPException(SnapBookHTTPException):
    status_code = 401
    detail = "Вы не ввели название или описание"

class FacilityEmptyDataHTTPException(SnapBookHTTPException):
    status_code = 401
    detail = "Вы не ввели название удобства"

class HotelAndRoomNotRelatedHTTPException(SnapBookHTTPException):
    status_code = 409
    detail = "Этот отель и номер не связаны"


class EmailNotRegisteredHTTPException(SnapBookHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectTokenHTTPException(SnapBookHTTPException):
    status_code = 401
    detail = "Некорректный токен"


class IncorrectPasswordHTTPException(SnapBookHTTPException):
    status_code = 401
    detail = "Пароль неверный"

class NoPasswordHTTPException(SnapBookHTTPException):
    status_code = 401
    detail = "Вы не указали пароль"

class UserNotAuthenticatedHTTPException(SnapBookHTTPException):
    status_code = 401
    detail = "Вы не вошли в аккаунт"


class NoAccessTokenHTTPException(SnapBookHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"



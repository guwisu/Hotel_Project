class SnapBookException(Exception):
    detail = "Неожиданная ошибка"


    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(SnapBookException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(SnapBookException):
    detail = "Не осталось свободных номеров"

class ConflictException(SnapBookException):
    detail = "Конфликт"

class UserAlreadyExistsException(SnapBookException):
    detail = "Пользователь с таким email уже существует"

class IncorrectDateException(SnapBookException):
    detail = "Неправильная дата"

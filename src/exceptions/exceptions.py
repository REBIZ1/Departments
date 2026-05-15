from fastapi import HTTPException


class BaseException(Exception):
    detail = "Ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectAlreadyExistsException(BaseException):
    detail = "Объект уже сущетсвует"


class DepartmentAlreadyExistsHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Подразделение уже существует"


class ObjectNotFoundException(BaseException):
    detail = "Объект не найден"


class DepartmentNotFoundException(BaseException):
    detail = "Подразделение не найдено"


class DepartmentNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Подразделение не найдено"

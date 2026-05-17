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


class DepartmentCannotBeSelfChildException(BaseException):
    detail = "Подразделение не может быть подразделом самого себя"


class DepartmentHierarchyLoopException(BaseException):
    detail = "Старший отдел не может быть дочерним для младшего"


class DepartmentCannotBeSelfChildHTTPException(BaseHTTPException):
    status_code = 400
    detail = "Подразделение не может быть подразделом самого себя"


class DepartmentHierarchyLoopHTTPException(BaseHTTPException):
    status_code = 400
    detail = "Старший отдел не может быть дочерним для младшего"


class SourceAndTargetDepartmentsAreSameException(BaseException):
    detail = "ID отдела для удаления и ID целевого отдела не должны совпадать"


class SourceAndTargetDepartmentsAreSameHTTPException(BaseHTTPException):
    status_code = 400
    detail = "ID отдела для удаления и ID целевого отдела не должны совпадать"

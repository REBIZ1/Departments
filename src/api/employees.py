from fastapi import APIRouter

from src.api.dependencies.dependencies import DBDep
from src.exceptions.exceptions import (
    DepartmentNotFoundException,
    DepartmentNotFoundHTTPException,
)
from src.schemas.employees import EmployeeAddRequest
from src.services.employees import EmployeeService

router = APIRouter(prefix="/departments", tags=["Работники"])


@router.post("/{id}/employees", summary="Добавить нового сотрудника в подразделение")
async def create_employee(db: DBDep, id: int, data: EmployeeAddRequest):
    """
    Создает работника в подразделении
    """
    try:
        employee = await EmployeeService(db).create_employee(id, data)
    except DepartmentNotFoundException:
        raise DepartmentNotFoundHTTPException
    return employee

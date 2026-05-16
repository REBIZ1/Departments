from fastapi import APIRouter, Query

from src.api.dependencies.dependencies import DBDep
from src.exceptions.exceptions import (
    ObjectAlreadyExistsException,
    DepartmentAlreadyExistsHTTPException,
    DepartmentNotFoundException,
    DepartmentNotFoundHTTPException,
)
from src.schemas.departments import DepartmentAdd
from src.services.departments import DepartmentService

router = APIRouter(prefix="/departments", tags=["Подразделения"])


@router.post("", summary="Создать подразделение")
async def create_department(db: DBDep, data: DepartmentAdd):
    """
    Создает подразделение
    """
    try:
        department = await DepartmentService(db).create_department(data)
    except ObjectAlreadyExistsException:
        raise DepartmentAlreadyExistsHTTPException
    except DepartmentNotFoundException:
        raise DepartmentNotFoundHTTPException
    return department


@router.get("/{id}", summary="Получить подразделения")
async def get_department(
    db: DBDep,
    id: int,
    depth: int = Query(default=1, ge=1, le=5),
    include_employees: bool = True,
):
    """
    Получить подразделения
    """
    try:
        department = await DepartmentService(db).get_department_tree(
            department_id=id,
            depth=depth,
            include_employees=include_employees,
        )
    except DepartmentNotFoundException:
        raise DepartmentNotFoundHTTPException
    return department

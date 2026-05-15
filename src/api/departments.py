from fastapi import APIRouter

from src.api.dependencies.dependencies import DBDep
from src.exceptions.exceptions import (
    ObjectAlreadyExistsException,
    DepartmentAlreadyExistsHTTPException,
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
    return department

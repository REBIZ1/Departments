from typing import Literal
from fastapi import APIRouter, Query, Response

from src.api.dependencies.dependencies import DBDep
from src.exceptions.exceptions import (
    ObjectAlreadyExistsException,
    DepartmentAlreadyExistsHTTPException,
    DepartmentNotFoundException,
    DepartmentNotFoundHTTPException,
    DepartmentCannotBeSelfChildException,
    DepartmentCannotBeSelfChildHTTPException,
    DepartmentHierarchyLoopException,
    DepartmentHierarchyLoopHTTPException,
    SourceAndTargetDepartmentsAreSameException,
    SourceAndTargetDepartmentsAreSameHTTPException,
)
from src.schemas.departments import DepartmentAdd, DepartmentPatch
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


@router.patch("/{id}", summary="Изменить подразделение")
async def update_department(db: DBDep, id: int, data: DepartmentPatch):
    """
    Изменяет подразделение
    """
    try:
        department = await DepartmentService(db).update_department(
            department_id=id, data=data
        )
    except DepartmentCannotBeSelfChildException:
        raise DepartmentCannotBeSelfChildHTTPException
    except DepartmentHierarchyLoopException:
        raise DepartmentHierarchyLoopHTTPException
    except DepartmentNotFoundException:
        raise DepartmentNotFoundHTTPException
    return department


@router.delete("/{id}", status_code=204, summary="Удалить подразделение")
async def delete_department(
    db: DBDep,
    id: int,
    mode: Literal["cascade", "reassign"],
    reassign_to_department_id: int | None = None,
):
    """
    Удаляет подразделение
    """
    try:
        await DepartmentService(db).delete_department(
            department_id=id,
            mode=mode,
            reassign_to_department_id=reassign_to_department_id,
        )
    except DepartmentNotFoundException:
        raise DepartmentNotFoundHTTPException
    except SourceAndTargetDepartmentsAreSameException:
        raise SourceAndTargetDepartmentsAreSameHTTPException
    return Response(status_code=204)

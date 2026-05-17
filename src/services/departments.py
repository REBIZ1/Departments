from src.exceptions.exceptions import (
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    DepartmentNotFoundException,
    DepartmentCannotBeSelfChildException,
    DepartmentHierarchyLoopException,
)
from src.schemas.departments import DepartmentAdd, DepartmentTree, DepartmentPatch
from src.services.base import BaseService


class DepartmentService(BaseService):
    async def get_department_with_check(self, department_id: int):
        """
        Проверяет существование подразделение
        """
        try:
            await self.db.departments.get_one(id=department_id)
        except ObjectNotFoundException:
            raise DepartmentNotFoundException

    async def create_department(self, data: DepartmentAdd):
        """
        Создает подразделение
        """
        existing_department = await self.db.departments.get_by_name_and_parent(
            data.name, data.parent_id
        )
        if existing_department:
            raise ObjectAlreadyExistsException
        if data.parent_id is not None:
            await self.get_department_with_check(data.parent_id)
        department = await self.db.departments.add(data)
        await self.db.commit()
        return department

    async def _build_tree(
        self,
        department,
        depth: int,
        include_employees: bool,
    ):
        """
        Рекурсивно строит дерево
        """
        employees = []
        if include_employees:
            employees = await self.db.employees.get_employees_from_department(
                department.id
            )
        children = []
        if depth > 0:
            child_departments = await self.db.departments.get_children(department.id)
            for child in child_departments:
                child_tree = await self._build_tree(
                    department=child,
                    depth=depth - 1,
                    include_employees=include_employees,
                )
                children.append(child_tree)
        return DepartmentTree(
            department=department,
            employees=employees,
            children=children,
        )

    async def get_department_tree(
        self, department_id: int, depth: int = 1, include_employees: bool = True
    ):
        """
        Получает дерево подразделений
        """
        await DepartmentService(self.db).get_department_with_check(department_id)
        department = await self.db.departments.get_one(id=department_id)
        return await self._build_tree(
            department=department, depth=depth, include_employees=include_employees
        )

    async def validate_no_cycle(self, department_id: int, parent_id: int):
        """
        Проверка на цикл в дереве
        """
        current_parent_id = parent_id
        while current_parent_id is not None:
            if current_parent_id == department_id:
                raise DepartmentHierarchyLoopException
            department = await self.db.departments.get_one(id=current_parent_id)
            current_parent_id = department.parent_id

    async def update_department(self, department_id: int, data: DepartmentPatch):
        """
        Изменяет подразделение
        """
        await self.get_department_with_check(department_id)
        update_data = data.model_dump(exclude_unset=True)
        if "parent_id" in update_data:
            parent_id = update_data["parent_id"]
            if parent_id == department_id:
                raise DepartmentCannotBeSelfChildException
            if parent_id is not None:
                await self.get_department_with_check(parent_id)
                await self.validate_no_cycle(
                    department_id=department_id,
                    parent_id=parent_id
                )
        updated_department = await self.db.departments.edit(
            data=data,
            exclude_unset=True,
            id=department_id
        )
        await self.db.commit()
        return updated_department

from src.exceptions.exceptions import (
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    DepartmentNotFoundException,
)
from src.schemas.departments import DepartmentAdd
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
        await self.get_department_with_check(data.parent_id)
        department = await self.db.departments.add(data)
        await self.db.commit()
        return department

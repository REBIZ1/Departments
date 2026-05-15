from src.exceptions.exceptions import ObjectAlreadyExistsException
from src.schemas.departments import DepartmentAdd
from src.services.base import BaseService


class DepartmentService(BaseService):
    async def create_department(self, data: DepartmentAdd):
        """
        Создает подразделение
        """
        existing_department = await self.db.departments.get_by_name_and_parent(
            data.name, data.parent_id
        )
        if existing_department:
            raise ObjectAlreadyExistsException
        department = await self.db.departments.add(data)
        await self.db.commit()
        return department

from sqlalchemy import select

from src.models import EmployeesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.employees import EmployeeDataMapper


class EmployeesRepository(BaseRepository):
    model = EmployeesOrm
    mapper = EmployeeDataMapper

    async def get_employees_from_department(self, department_id: int):
        """
        Получить работников подразделения
        """
        query = (
            select(self.model)
            .filter_by(department_id=department_id)
            .order_by(self.model.created_at)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(obj) for obj in result.scalars().all()]

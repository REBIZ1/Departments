from sqlalchemy import select

from src.models import DepartmentsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.departments import DepartmentDataMapper


class DepartmentsRepository(BaseRepository):
    model = DepartmentsOrm
    mapper = DepartmentDataMapper

    async def get_by_name_and_parent(self, name: str, parent_id: int | None = None):
        """
        Выполняет поиск по имени и parent_id.
        Используется для проверки уникальности
        """
        query = select(self.model).where(
            self.model.name == name, self.model.parent_id == parent_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

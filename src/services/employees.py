from src.schemas.employees import EmployeeAddRequest, EmployeeAdd
from src.services.base import BaseService
from src.services.departments import DepartmentService


class EmployeeService(BaseService):
    async def create_employee(self, id: int, data: EmployeeAddRequest):
        """
        Создает работника в подразделении
        """
        await DepartmentService(self.db).get_department_with_check(id)
        _data = EmployeeAdd(department_id=id, **data.model_dump())
        employee = await self.db.employees.add(_data)
        await self.db.commit()
        return employee

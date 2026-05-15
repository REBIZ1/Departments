from src.models import EmployeesOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.employees import Employee


class EmployeeDataMapper(DataMapper):
    db_model = EmployeesOrm
    schema = Employee

from src.models import EmployeesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.employees import EmployeeDataMapper


class EmployeesRepository(BaseRepository):
    model = EmployeesOrm
    mapper = EmployeeDataMapper

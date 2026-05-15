from src.models import DepartmentsOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.departments import Department


class DepartmentDataMapper(DataMapper):
    db_model = DepartmentsOrm
    schema = Department

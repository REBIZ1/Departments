from datetime import date
from pydantic import BaseModel, Field, field_validator


class EmployeeAddRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)
    hired_at: date | None = None

    @field_validator("full_name", "position")
    @classmethod
    def validate_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Поле не может быть пустым")
        return value


class EmployeeAdd(EmployeeAddRequest):
    department_id: int


class Employee(EmployeeAdd):
    id: int

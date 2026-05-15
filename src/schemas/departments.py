from pydantic import BaseModel, Field, field_validator


class DepartmentAdd(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    parent_id: int | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("Подразделение не может быть пустым")
        return value


class Department(DepartmentAdd):
    id: int


class DepartmentPatch(DepartmentAdd):
    name: str | None = Field(None, min_length=1, max_length=200)

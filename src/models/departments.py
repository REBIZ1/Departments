from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, String, UniqueConstraint, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class DepartmentsOrm(Base):
    __tablename__ = "departments"

    __table_args__ = (
        UniqueConstraint("parent_id", "name", name="unique_department"),
        CheckConstraint("length(name) >= 1", name="check_department_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    parent: Mapped["DepartmentsOrm"] = relationship(
        "DepartmentsOrm", remote_side=[id], back_populates="children"
    )
    children: Mapped[list["DepartmentsOrm"]] = relationship(
        "DepartmentsOrm",
        back_populates="parent",
        cascade="all, delete",
        passive_deletes=True,
    )
    employees: Mapped[list["EmployeesOrm"]] = relationship(
        "EmployeesOrm",
        back_populates="department",
        cascade="all, delete",
        passive_deletes=True,
    )

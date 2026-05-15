from datetime import datetime, date
from sqlalchemy import ForeignKey, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class EmployeesOrm(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"), index=True
    )
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[str] = mapped_column(String(200), nullable=False)
    hired_at: Mapped[date | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    department: Mapped["DepartmentsOrm"] = relationship(
        "DepartmentsOrm", back_populates="employees"
    )

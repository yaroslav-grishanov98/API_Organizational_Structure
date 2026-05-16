import logging
from datetime import date
from sqlalchemy.orm import Session
from app.exceptions import not_found
from app.models.employee import Employee
from app.repositories.department import DepartmentRepository
from app.repositories.employee import EmployeeRepository


logger = logging.getLogger(__name__)


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
        self.dept_repo = DepartmentRepository(db)
        self.emp_repo = EmployeeRepository(db)

    def create(
        self,
        department_id: int,
        full_name: str,
        position: str,
        hired_at: date | None,
    ) -> Employee:
        department = self.dept_repo.get_by_id(department_id)
        if not department:
            raise not_found("Отдел не найден")

        logger.info(
            f"Создание сотрудника '{full_name}' в подразделении id={department_id}"
        )
        return self.emp_repo.create(
            department_id=department_id,
            full_name=full_name,
            position=position,
            hired_at=hired_at,
        )

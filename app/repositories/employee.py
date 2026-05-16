from sqlalchemy.orm import Session
from app.models.employee import Employee


class EmployeeRepository:
    """Репозиторий сотрудников"""
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, employee_id: int) -> Employee | None:
        """Получить сотрудника по айди"""
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def get_by_department_id(self, department_id: int) -> list[Employee]:
        """Найти сотрудника по айди отдела"""
        return (
            self.db.query(Employee)
            .filter(Employee.department_id == department_id)
            .order_by(Employee.full_name)
            .all()
        )

    def create(
        self,
        department_id: int,
        full_name: str,
        position: str,
        hired_at=None,
    ) -> Employee:
        """Создать сотрудника"""
        employee = Employee(
            department_id=department_id,
            full_name=full_name,
            position=position,
            hired_at=hired_at,
        )
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def reassign_to_department(self, from_department_id: int, to_department_id: int) -> None:
        """Переводит сотрудников из одного подразделения в другое"""
        self.db.query(Employee).filter(
            Employee.department_id == from_department_id
        ).update({"department_id": to_department_id})
        self.db.commit()

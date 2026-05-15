from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.department import Department


class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, department_id: int) -> Department | None:
        return self.db.query(Department).filter(Department.id == department_id).first()

    def get_by_name_and_parent(
            self, name: str, parent_id: int | None, exclude_id: int | None = None
    ) -> Department | None:
        query = self.db.query(Department).filter(
            and_(Department.name == name, Department.parent_id == parent_id)
        )
        if exclude_id is not None:
            query = query.filter(Department.id !=exclude_id)
            return query.first()

    def create(self, name: str, parent_id: int | None) -> Department:
        department = Department(name=name, parent_id=parent_id)
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)
        return department

    def update(self, department: Department, **kwargs) -> Department:
        for key, value in kwargs.items():
            setattr(department, key, value)
        self.db.commit()
        self.db.refresh(department)
        return department

    def delete(self, department: Department) -> None:
        self.db.delete(department)
        self.db.commit()

    def get_all_descendant_ids(self, department_id: int) -> set[int]:
        """Собирает все id дочерних подразделений"""
        result = set()
        queue = [department_id]
        while queue:
            current_id = queue.pop()
            children = (
                self.db.query(Department.id)
                .filter(Department.parent_id == current_id)
                .all()
            )
            for (child_id,) in children:
                result.add(child_id)
                queue.append(child_id)
        return result

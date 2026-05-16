import logging
from sqlalchemy.orm import Session
from app.exceptions import bad_request, conflict, not_found
from app.models.department import Department
from app.repositories.department import DepartmentRepository
from app.repositories.employee import EmployeeRepository
from app.schemas.department import DepartmentDetail, DepartmentResponse


logger = logging.getLogger(__name__)

class DepartmentService:
    def __init__(self, db: Session):
        self.db = db
        self.dept_repo = DepartmentRepository(db)
        self.emp_repo = EmployeeRepository(db)

    def create(self, name: str, parent_id: int | None) -> Department:
        if parent_id is not None:
            parent = self.dept_repo.get_by_id(parent_id)
            if not parent:
                raise not_found("Отдел не найден")

        existing = self.dept_repo.get_by_name_and_parent(name, parent_id)
        if existing:
            raise conflict(
                f"Отдел с таким именем '{name}' уже существует"
            )

        logger.info(f"Создать отдел с именем '{name}' от родительского {parent_id}")
        return self.dept_repo.create(name=name, parent_id=parent_id)

    def get_detail(
            self, department_id: int, depth: int, include_employees: bool
    ) -> DepartmentDetail:
        department = self.dept_repo.get_by_id(department_id)
        if not department:
            raise not_found("Отдел не найден")

        return self._build_tree(department, depth, include_employees)

    def _build_tree(
            self, department: Department, depth: int, include_employees: bool
    ) -> DepartmentDetail:
        employees = []
        if include_employees:
            employees = self.emp_repo.get_by_department_id(department.id)

        children = []
        if depth > 0:
            for child in department.children:
                children.append(
                    self._build_tree(child, depth - 1, include_employees)
                )

        return DepartmentDetail(
            id=department.id,
            name=department.name,
            parent_id=department.parent_id,
            created_at=department.created_at,
            employees=[e for e in employees],
            children=children,
        )

    def update(self, department_id: int, **kwargs) -> Department:
        department = self.dept_repo.get_by_id(department_id)
        if not department:
            raise not_found("Отдел не найден")

        new_name = kwargs.get("name")
        new_parent_id = kwargs.get("parent_id", department.parent_id)

        if "parent_id" in kwargs and kwargs["parent_id"] == department_id:
            raise bad_request("Отдел не может быть самостоятельным")

        if "parent_id" in kwargs and kwargs["parent_id"] is not None:
            descendant_ids = self.dept_repo.get_all_descendant_ids(department_id)
            if kwargs["parent_id"] in descendant_ids:
                raise conflict("Невозможно перенести отдел внутрь своего поддерева")
            new_parent = self.dept_repo.get_by_id(kwargs["parent_id"])
            if not new_parent:
                raise not_found("Отдел не найден")

        check_name = new_name if new_name else department.name # Уникальность имени
        check_parent = new_parent_id

        existing = self.dept_repo.get_by_name_and_parent(
            check_name, check_parent, exclude_id=department_id
        )
        if existing:
            raise conflict("Отдел с таким названием уже существует")

        update_data = {k: v for k, v in kwargs.items() if v is not None} # Убираем из kwargs ключи со значением None чтобы не затирать поля

        logger.info(f"Обновление данных {department_id} от даты {update_data}")
        return self.dept_repo.update(department, **update_data)

    def delete(
            self, department_id: int, mode: str, reassign_to_department_id: int | None,
    ) -> None:
        department = self.dept_repo.get_by_id(department_id)
        if not department:
            raise not_found("Отдел не найден")

        if mode == "reassign":
            if reassign_to_department_id is None:
                raise bad_request(
                    "reassign_to_department_id обязателен при mode=reassign"
                )

            target = self.dept_repo.get_by_id(reassign_to_department_id)
            if not target:
                raise not_found("Целевой отдел для переназначения не найден")

            if reassign_to_department_id == department_id:
                raise bad_request("Невозможно переназначить сотрудников в отдел")

            self.emp_repo.reassign_to_department(department_id, reassign_to_department_id) # Переводим сотрудников
            logger.info(
                f"Сотрудники переведены из подразделения {department_id} "
                f"в подразделение {reassign_to_department_id}"
            )

        elif mode == "cascade":
            logger.info(f"Каскадное удаление подразделения id={department_id}")

        else:
            raise bad_request("Режим должен быть 'cascade' или 'reassign'")

        self.dept_repo.delete(department)

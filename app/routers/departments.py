import logging
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.department import DepartmentCreate, DepartmentDetail, DepartmentUpdate, DepartmentResponse
from app.schemas.employee import EmployeeCreate, EmployeeResponse
from app.services.department import DepartmentService
from app.services.employee import EmployeeService


router = APIRouter(prefix="/departments", tags=["Departments"])

logger = logging.getLogger(__name__)

@router.post("/", response_model=DepartmentResponse, status_code=201)
def create_department(
        body: DepartmentCreate,
        db: Session = Depends(get_db),
):
    service = DepartmentService(db)
    return service.create(name=body.name, parent_id=body.parent_id)

@router.post("/{department_id}/employees/", response_model=EmployeeResponse, status_code=201)
def create_employee(
        department_id: int,
        body: EmployeeCreate,
        db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    return service.create(
        department_id=department_id,
        full_name=body.full_name,
        position=body.position,
        hired_at=body.hired_at,
    )

@router.get("/{department_id}", response_model=DepartmentDetail)
def get_department(
        department_id: int,
        depth: int=Query(default=1, ge=0, le=5),
        include_employees: bool = Query(default=True),
        db: Session = Depends(get_db),
):
    service = DepartmentService(db)
    return service.get_detail(
        department_id=department_id,
        depth=depth,
        include_employees=include_employees,
    )

@router.patch("/{department_id}", response_model=DepartmentResponse)
def update_department(
        department_id: int,
        body: DepartmentUpdate,
        db: Session = Depends(get_db),
):
    service = DepartmentService(db)
    update_data = body.model_dump(exclude_unset=True)
    return service.update(department_id, **update_data)

@router.delete("/{department_id}", status_code=204)
def delete_department(
        department_id: int,
        mode: str = Query(..., pattern="^(cascade|reassign)$"),
        reassign_to_department_id: int | None = Query(default=None),
        db: Session = Depends(get_db),
):
    service = DepartmentService(db)
    service.delete(
        department_id=department_id,
        mode=mode,
        reassign_to_department_id=reassign_to_department_id,
    )
    return Response(status_code=204)

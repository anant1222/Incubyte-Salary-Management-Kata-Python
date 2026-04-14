from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.repositories import employee_repository
from app.schemas.employee import EmployeeCreate, EmployeeRead


def create_employee(db: Session, payload: EmployeeCreate) -> EmployeeRead:
    employee = Employee(**payload.model_dump())
    employee_repository.create(db, employee)
    return EmployeeRead.model_validate(employee)

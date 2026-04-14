from sqlalchemy.orm import Session

from app.repositories import employee_repository
from app.schemas.employee import EmployeeCreate, EmployeeRead


def create_employee(db: Session, payload: EmployeeCreate) -> EmployeeRead:
    created = employee_repository.create(db, **payload.model_dump())
    return EmployeeRead.model_validate(created)

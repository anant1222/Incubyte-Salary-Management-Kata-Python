from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.repositories import employee_repository
from app.schemas.employee import EmployeeCreate, EmployeeRead


def get_employee_by_id(db: Session, employee_id: int) -> EmployeeRead:
    employee = employee_repository.get_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeRead.model_validate(employee)


def create_employee(db: Session, payload: EmployeeCreate) -> EmployeeRead:
    employee = Employee(**payload.model_dump())
    employee_repository.create(db, employee)
    return EmployeeRead.model_validate(employee)


def update_employee(db: Session, employee_id: int, payload: EmployeeCreate) -> EmployeeRead:
    employee = employee_repository.get_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    data = payload.model_dump()
    employee.full_name = data["full_name"]
    employee.job_title = data["job_title"]
    employee.country = data["country"]
    employee.salary = data["salary"]
    employee_repository.update(db, employee)
    return EmployeeRead.model_validate(employee)

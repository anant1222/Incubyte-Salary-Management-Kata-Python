from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.repositories import employee_repository
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeSalaryBreakdown
from app.services.salary_service import deduction_for_country


def _require_employee(db: Session, employee_id: int) -> Employee:
    employee = employee_repository.get_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


def get_employee_by_id(db: Session, employee_id: int) -> EmployeeRead:
    employee = _require_employee(db, employee_id)
    return EmployeeRead.model_validate(employee)


def get_employee_salary_breakdown(db: Session, employee_id: int) -> EmployeeSalaryBreakdown:
    employee = _require_employee(db, employee_id)
    gross = employee.salary
    deduction = deduction_for_country(employee.country, gross)
    return EmployeeSalaryBreakdown(
        employee_id=employee.id,
        gross_salary=gross,
        deduction=deduction,
        net_salary=gross - deduction,
    )


def create_employee(db: Session, payload: EmployeeCreate) -> EmployeeRead:
    employee = Employee(**payload.model_dump())
    employee_repository.create(db, employee)
    return EmployeeRead.model_validate(employee)


def update_employee(db: Session, employee_id: int, payload: EmployeeCreate) -> EmployeeRead:
    employee = _require_employee(db, employee_id)
    for key, value in payload.model_dump().items():
        setattr(employee, key, value)
    employee_repository.update(db, employee)
    return EmployeeRead.model_validate(employee)


def delete_employee(db: Session, employee_id: int) -> None:
    employee = _require_employee(db, employee_id)
    employee_repository.delete(db, employee)

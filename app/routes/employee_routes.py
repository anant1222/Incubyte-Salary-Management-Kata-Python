from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success_response
from app.db.database import get_db
from app.schemas.employee import EmployeeCreate
from app.services import employee_service

router = APIRouter(tags=["employees"])


@router.get("/employees/{employee_id}/salary", status_code=200)
def get_employee_salary(
    employee_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    breakdown = employee_service.get_employee_salary_breakdown(db, employee_id)
    return success_response(
        message="Employee salary fetched successfully",
        status_code=200,
        data=breakdown.model_dump(mode="json"),
    )


@router.get("/employees/{employee_id}", status_code=200)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    employee_read = employee_service.get_employee_by_id(db, employee_id)
    return success_response(
        message="Employee fetched successfully",
        status_code=200,
        data=employee_read.model_dump(mode="json"),
    )


@router.delete("/employees/{employee_id}", status_code=200)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    employee_service.delete_employee(db, employee_id)
    return success_response(
        message="Employee deleted successfully",
        status_code=200,
        data={},
    )


@router.put("/employees/{employee_id}", status_code=200)
def update_employee(
    employee_id: int,
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    employee_read = employee_service.update_employee(db, employee_id, payload)
    return success_response(
        message="Employee updated successfully",
        status_code=200,
        data=employee_read.model_dump(mode="json"),
    )


@router.post("/employees", status_code=201)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    employee_read = employee_service.create_employee(db, payload)
    return success_response(
        message="Employee created successfully",
        status_code=201,
        data=employee_read.model_dump(mode="json"),
    )

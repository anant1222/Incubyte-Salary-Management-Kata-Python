from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success_response
from app.db.database import get_db
from app.schemas.employee import EmployeeCreate
from app.services import employee_service

router = APIRouter(tags=["employees"])


@router.post("/employees", status_code=201)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    data = employee_service.create_employee(db, payload)
    return success_response(
        message="Employee created successfully",
        status_code=201,
        data=data.model_dump(mode="json"),
    )

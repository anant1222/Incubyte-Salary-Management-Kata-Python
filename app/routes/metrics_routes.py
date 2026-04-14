from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import success_response
from app.db.database import get_db
from app.services import metrics_service

router = APIRouter(tags=["metrics"])


@router.get("/metrics/country", status_code=200)
def get_country_metrics(
    name: str = Query(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    metrics = metrics_service.country_salary_metrics(db, name)
    return success_response(
        message="Country salary metrics fetched successfully",
        status_code=200,
        data=metrics.model_dump(mode="json"),
    )

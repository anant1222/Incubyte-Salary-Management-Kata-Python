from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import success_response
from app.db.database import get_db
from app.services import metrics_service

router = APIRouter(tags=["metrics"])


@router.get("/metrics/job", status_code=200)
def get_job_metrics(
    title: str = Query(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    job_title_metrics = metrics_service.job_title_salary_metrics(db, job_title=title)
    return success_response(
        message="Job title salary metrics fetched successfully",
        status_code=200,
        data=job_title_metrics.model_dump(mode="json"),
    )


@router.get("/metrics/country", status_code=200)
def get_country_metrics(
    name: str = Query(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    country_metrics = metrics_service.country_salary_metrics(db, name)
    return success_response(
        message="Country salary metrics fetched successfully",
        status_code=200,
        data=country_metrics.model_dump(mode="json"),
    )

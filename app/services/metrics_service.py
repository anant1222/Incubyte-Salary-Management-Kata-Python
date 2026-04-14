from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import employee_repository
from app.schemas.metrics import CountrySalaryMetrics


def country_salary_metrics(db: Session, country: str) -> CountrySalaryMetrics:
    salaries = employee_repository.list_salaries_for_country(db, country)
    if not salaries:
        raise HTTPException(
            status_code=404,
            detail="No employees found for the given country",
        )
    count = len(salaries)
    min_salary = min(salaries)
    max_salary = max(salaries)
    avg_salary = sum(salaries) // count
    return CountrySalaryMetrics(
        country=country,
        min_salary=min_salary,
        max_salary=max_salary,
        avg_salary=avg_salary,
    )

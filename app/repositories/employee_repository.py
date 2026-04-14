from sqlalchemy.orm import Session

from app.models.employee import Employee


def create(db: Session, *, full_name: str, job_title: str, country: str, salary: int) -> Employee:
    employee = Employee(
        full_name=full_name,
        job_title=job_title,
        country=country,
        salary=salary,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

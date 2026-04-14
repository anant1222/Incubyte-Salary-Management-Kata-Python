from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employee import Employee


def get_by_id(db: Session, employee_id: int) -> Employee | None:
    return db.get(Employee, employee_id)


def list_salaries_for_country(db: Session, country: str) -> list[int]:
    statement = select(Employee.salary).where(Employee.country == country)
    return list(db.scalars(statement).all())


def create(db: Session, employee: Employee) -> Employee:
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update(db: Session, employee: Employee) -> Employee:
    db.commit()
    db.refresh(employee)
    return employee


def delete(db: Session, employee: Employee) -> None:
    db.delete(employee)
    db.commit()

from sqlalchemy.orm import Session

from app.models.employee import Employee


def get_by_id(db: Session, employee_id: int) -> Employee | None:
    return db.get(Employee, employee_id)


def create(db: Session, employee: Employee) -> Employee:
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

from sqlalchemy.orm import Session

from app.models.employee import Employee


def create(db: Session, employee: Employee) -> Employee:
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

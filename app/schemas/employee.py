from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class EmployeeCreate(BaseModel):
    full_name: str
    job_title: str
    country: str
    salary: int

    @field_validator("full_name")
    @classmethod
    def full_name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("full_name cannot be empty")
        return v.strip()

    @field_validator("salary", mode="before")
    @classmethod
    def salary_valid(cls, v: Any) -> int:
        if isinstance(v, bool):
            raise ValueError("salary must be a number")
        if isinstance(v, int):
            if v < 0:
                raise ValueError("salary must be zero or greater")
            return v
        if isinstance(v, str):
            try:
                n = int(v, 10)
            except ValueError:
                raise ValueError("salary must be a number") from None
            if n < 0:
                raise ValueError("salary must be zero or greater")
            return n
        if isinstance(v, float):
            if not v.is_integer():
                raise ValueError("salary must be a number")
            n = int(v)
            if n < 0:
                raise ValueError("salary must be zero or greater")
            return n
        raise ValueError("salary must be a number")


class EmployeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    job_title: str
    country: str
    salary: int

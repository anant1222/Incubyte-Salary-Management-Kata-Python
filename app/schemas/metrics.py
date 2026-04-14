from pydantic import BaseModel


class CountrySalaryMetrics(BaseModel):
    country: str
    min_salary: int
    max_salary: int
    avg_salary: int

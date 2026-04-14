from pydantic import BaseModel


class CountrySalaryMetrics(BaseModel):
    country: str
    min_salary: int
    max_salary: int
    avg_salary: int


class JobTitleSalaryMetrics(BaseModel):
    job_title: str
    avg_salary: int

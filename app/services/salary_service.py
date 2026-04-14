def deduction_for_country(country: str, gross_salary: int) -> int:
    if country == "India":
        return (gross_salary * 10) // 100
    if country == "United States":
        return (gross_salary * 12) // 100
    return 0

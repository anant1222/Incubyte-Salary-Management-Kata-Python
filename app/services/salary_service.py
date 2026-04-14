def breakdown_for_country(country: str, gross_salary: int) -> tuple[int, int]:
    if country == "India":
        deduction = (gross_salary * 10) // 100
    elif country == "United States":
        deduction = (gross_salary * 12) // 100
    else:
        deduction = 0
    net_salary = gross_salary - deduction
    return deduction, net_salary

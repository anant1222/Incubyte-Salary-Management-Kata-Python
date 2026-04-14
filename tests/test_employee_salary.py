from fastapi.testclient import TestClient

_GROSS = 100_000

_EMPLOYEE_INDIA = {
    "full_name": "Anant",
    "job_title": "Backend Engineer",
    "country": "India",
    "salary": _GROSS,
}

_EMPLOYEE_US = {
    "full_name": "Jordan",
    "job_title": "Backend Engineer",
    "country": "United States",
    "salary": _GROSS,
}

_EMPLOYEE_GERMANY = {
    "full_name": "Hans",
    "job_title": "Backend Engineer",
    "country": "Germany",
    "salary": _GROSS,
}


def _create_employee_id(client: TestClient, body: dict) -> int:
    created = client.post("/employees", json=body)
    assert created.status_code == 201
    return created.json()["data"]["id"]


def _assert_salary_success(
    response,
    *,
    employee_id: int,
    deduction: int,
    net_salary: int,
) -> None:
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Employee salary fetched successfully",
        "statusCode": 200,
        "data": {
            "employee_id": employee_id,
            "gross_salary": _GROSS,
            "deduction": deduction,
            "net_salary": net_salary,
        },
    }


def test_employee_salary_returns_breakdown_for_india(client: TestClient) -> None:
    employee_id = _create_employee_id(client, _EMPLOYEE_INDIA)

    response = client.get(f"/employees/{employee_id}/salary")

    _assert_salary_success(
        response,
        employee_id=employee_id,
        deduction=10_000,
        net_salary=90_000,
    )


def test_employee_salary_returns_breakdown_for_united_states(client: TestClient) -> None:
    employee_id = _create_employee_id(client, _EMPLOYEE_US)

    response = client.get(f"/employees/{employee_id}/salary")

    _assert_salary_success(
        response,
        employee_id=employee_id,
        deduction=12_000,
        net_salary=88_000,
    )


def test_employee_salary_returns_zero_deduction_for_other_country(client: TestClient) -> None:
    employee_id = _create_employee_id(client, _EMPLOYEE_GERMANY)

    response = client.get(f"/employees/{employee_id}/salary")

    _assert_salary_success(
        response,
        employee_id=employee_id,
        deduction=0,
        net_salary=_GROSS,
    )


def test_employee_salary_returns_404_when_employee_does_not_exist(client: TestClient) -> None:
    response = client.get("/employees/999999999/salary")

    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "message": "Employee not found",
        "statusCode": 404,
        "data": {},
    }

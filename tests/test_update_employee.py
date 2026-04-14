from fastapi.testclient import TestClient

_SEED = {
    "full_name": "Anant",
    "job_title": "Backend Engineer",
    "country": "India",
    "salary": 120000,
}

_UPDATE = {
    "full_name": "Anant Verma",
    "job_title": "Senior Backend Engineer",
    "country": "United States",
    "salary": 150000,
}


def _create_employee_id(client: TestClient) -> int:
    created = client.post("/employees", json=_SEED)
    assert created.status_code == 201
    return created.json()["data"]["id"]


def _assert_error(response, *, status_code: int, message: str) -> None:
    assert response.status_code == status_code
    assert response.json() == {
        "success": False,
        "message": message,
        "statusCode": status_code,
        "data": {},
    }


def test_update_employee_returns_200_when_employee_exists(client: TestClient) -> None:
    employee_id = _create_employee_id(client)

    response = client.put(f"/employees/{employee_id}", json=_UPDATE)

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Employee updated successfully",
        "statusCode": 200,
        "data": {
            "id": employee_id,
            "full_name": "Anant Verma",
            "job_title": "Senior Backend Engineer",
            "country": "United States",
            "salary": 150000,
        },
    }


def test_update_employee_returns_404_when_employee_does_not_exist(client: TestClient) -> None:
    response = client.put("/employees/999999999", json=_UPDATE)

    _assert_error(response, status_code=404, message="Employee not found")


def test_update_employee_returns_400_for_invalid_payload(client: TestClient) -> None:
    employee_id = _create_employee_id(client)
    bad = {**_UPDATE, "salary": "not a number"}

    response = client.put(f"/employees/{employee_id}", json=bad)

    _assert_error(response, status_code=400, message="salary must be a number")


def test_update_employee_returns_400_when_salary_is_negative(client: TestClient) -> None:
    employee_id = _create_employee_id(client)
    bad = {**_UPDATE, "salary": -1}

    response = client.put(f"/employees/{employee_id}", json=bad)

    _assert_error(response, status_code=400, message="salary must be zero or greater")


def test_update_employee_returns_400_when_required_field_is_missing(client: TestClient) -> None:
    employee_id = _create_employee_id(client)
    bad = {k: v for k, v in _UPDATE.items() if k != "full_name"}

    response = client.put(f"/employees/{employee_id}", json=bad)

    _assert_error(response, status_code=400, message="full_name is required")

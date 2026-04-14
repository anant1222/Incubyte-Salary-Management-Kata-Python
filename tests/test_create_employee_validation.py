from fastapi.testclient import TestClient

_VALID_BODY = {
    "full_name": "Anant",
    "job_title": "Backend Engineer",
    "country": "India",
    "salary": 120000,
}


def _assert_bad_request(response, *, message: str) -> None:
    assert response.status_code == 400
    assert response.json() == {
        "success": False,
        "message": message,
        "statusCode": 400,
        "data": {},
    }


def test_create_employee_rejects_missing_full_name(client: TestClient) -> None:
    payload = {k: v for k, v in _VALID_BODY.items() if k != "full_name"}
    response = client.post("/employees", json=payload)
    _assert_bad_request(response, message="full_name is required")


def test_create_employee_rejects_missing_job_title(client: TestClient) -> None:
    payload = {k: v for k, v in _VALID_BODY.items() if k != "job_title"}
    response = client.post("/employees", json=payload)
    _assert_bad_request(response, message="job_title is required")


def test_create_employee_rejects_missing_country(client: TestClient) -> None:
    payload = {k: v for k, v in _VALID_BODY.items() if k != "country"}
    response = client.post("/employees", json=payload)
    _assert_bad_request(response, message="country is required")


def test_create_employee_rejects_missing_salary(client: TestClient) -> None:
    payload = {k: v for k, v in _VALID_BODY.items() if k != "salary"}
    response = client.post("/employees", json=payload)
    _assert_bad_request(response, message="salary is required")


def test_create_employee_rejects_negative_salary(client: TestClient) -> None:
    payload = {**_VALID_BODY, "salary": -1}
    response = client.post("/employees", json=payload)
    _assert_bad_request(response, message="salary must be zero or greater")


def test_create_employee_rejects_non_numeric_salary(client: TestClient) -> None:
    payload = {**_VALID_BODY, "salary": "not a number"}
    response = client.post("/employees", json=payload)
    _assert_bad_request(response, message="salary must be a number")


def test_create_employee_rejects_empty_full_name(client: TestClient) -> None:
    payload = {**_VALID_BODY, "full_name": ""}
    response = client.post("/employees", json=payload)
    _assert_bad_request(response, message="full_name cannot be empty")

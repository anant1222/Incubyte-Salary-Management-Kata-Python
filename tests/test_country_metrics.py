from fastapi.testclient import TestClient

_INDIA_EMPLOYEES = [
    {
        "full_name": "Anant",
        "job_title": "Backend Engineer",
        "country": "India",
        "salary": 100_000,
    },
    {
        "full_name": "Kajal",
        "job_title": "Backend Engineer",
        "country": "India",
        "salary": 120_000,
    },
    {
        "full_name": "priya",
        "job_title": "Backend Engineer",
        "country": "India",
        "salary": 80_000,
    },
]

_US_EMPLOYEE = {
    "full_name": "Jordan",
    "job_title": "Backend Engineer",
    "country": "United States",
    "salary": 150_000,
}


def _seed_employees_for_india_metrics(client: TestClient) -> None:
    for body in _INDIA_EMPLOYEES:
        created = client.post("/employees", json=body)
        assert created.status_code == 201
    us = client.post("/employees", json=_US_EMPLOYEE)
    assert us.status_code == 201


def _assert_not_found(response) -> None:
    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "message": "No employees found for the given country",
        "statusCode": 404,
        "data": {},
    }


def _assert_bad_request(response, *, message: str) -> None:
    assert response.status_code == 400
    assert response.json() == {
        "success": False,
        "message": message,
        "statusCode": 400,
        "data": {},
    }


def test_country_metrics_returns_min_max_avg_for_india(client: TestClient) -> None:
    _seed_employees_for_india_metrics(client)

    response = client.get("/metrics/country", params={"name": "India"})

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Country salary metrics fetched successfully",
        "statusCode": 200,
        "data": {
            "country": "India",
            "min_salary": 80_000,
            "max_salary": 120_000,
            "avg_salary": 100_000,
        },
    }


def test_country_metrics_returns_404_when_no_employees_for_country(client: TestClient) -> None:
    _seed_employees_for_india_metrics(client)

    response = client.get("/metrics/country", params={"name": "Germany"})

    _assert_not_found(response)


def test_country_metrics_returns_400_when_country_param_missing(client: TestClient) -> None:
    response = client.get("/metrics/country")

    _assert_bad_request(response, message="name is required")

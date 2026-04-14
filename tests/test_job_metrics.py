from fastapi.testclient import TestClient

_BACKEND_ENGINEERS = [
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
        "full_name": "Priya",
        "job_title": "Backend Engineer",
        "country": "India",
        "salary": 140_000,
    },
]

_PRODUCT_MANAGER = {
    "full_name": "Jordan",
    "job_title": "Product Manager",
    "country": "United States",
    "salary": 150_000,
}


def _seed_employees_for_job_metrics(client: TestClient) -> None:
    for body in _BACKEND_ENGINEERS:
        created = client.post("/employees", json=body)
        assert created.status_code == 201
    pm = client.post("/employees", json=_PRODUCT_MANAGER)
    assert pm.status_code == 201


def _assert_not_found(response) -> None:
    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "message": "No employees found for the given job title",
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


def test_job_metrics_returns_average_salary_for_title(client: TestClient) -> None:
    _seed_employees_for_job_metrics(client)

    response = client.get("/metrics/job", params={"title": "Backend Engineer"})

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Job title salary metrics fetched successfully",
        "statusCode": 200,
        "data": {
            "job_title": "Backend Engineer",
            "avg_salary": 120_000,
        },
    }


def test_job_metrics_returns_404_when_no_employees_for_job_title(client: TestClient) -> None:
    _seed_employees_for_job_metrics(client)

    response = client.get("/metrics/job", params={"title": "Data Scientist"})

    _assert_not_found(response)


def test_job_metrics_returns_400_when_title_param_missing(client: TestClient) -> None:
    response = client.get("/metrics/job")

    _assert_bad_request(response, message="title is required")

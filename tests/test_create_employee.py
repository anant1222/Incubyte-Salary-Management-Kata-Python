from fastapi.testclient import TestClient


def test_create_employee_returns_201_and_unified_envelope(client: TestClient) -> None:
    payload = {
        "full_name": "Anant",
        "job_title": "Backend Engineer",
        "country": "India",
        "salary": 120000,
    }

    response = client.post("/employees", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Employee created successfully"
    assert body["statusCode"] == 201

    data = dict(body["data"])
    employee_id = data.pop("id")
    assert isinstance(employee_id, int)
    assert data == {
        "full_name": "Anant",
        "job_title": "Backend Engineer",
        "country": "India",
        "salary": 120000,
    }

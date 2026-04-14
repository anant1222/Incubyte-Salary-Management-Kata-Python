from fastapi.testclient import TestClient

_SEED = {
    "full_name": "Anant",
    "job_title": "Backend Engineer",
    "country": "India",
    "salary": 120000,
}


def _create_employee_id(client: TestClient) -> int:
    created = client.post("/employees", json=_SEED)
    assert created.status_code == 201
    return created.json()["data"]["id"]


def test_get_employee_returns_200_when_employee_exists(client: TestClient) -> None:
    employee_id = _create_employee_id(client)

    response = client.get(f"/employees/{employee_id}")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Employee fetched successfully",
        "statusCode": 200,
        "data": {
            "id": employee_id,
            "full_name": "Anant",
            "job_title": "Backend Engineer",
            "country": "India",
            "salary": 120000,
        },
    }


def test_get_employee_returns_404_when_employee_does_not_exist(client: TestClient) -> None:
    response = client.get("/employees/999999999")

    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "message": "Employee not found",
        "statusCode": 404,
        "data": {},
    }


def test_get_employee_returns_400_when_id_is_not_an_integer(client: TestClient) -> None:
    response = client.get("/employees/not-an-id")

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["statusCode"] == 400
    assert body["data"] == {}
    assert isinstance(body["message"], str)
    assert body["message"]

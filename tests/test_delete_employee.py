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


def test_delete_employee_returns_200_when_employee_exists(client: TestClient) -> None:
    employee_id = _create_employee_id(client)

    response = client.delete(f"/employees/{employee_id}")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Employee deleted successfully",
        "statusCode": 200,
        "data": {},
    }


def test_delete_employee_returns_404_when_employee_does_not_exist(client: TestClient) -> None:
    response = client.delete("/employees/999999999")

    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "message": "Employee not found",
        "statusCode": 404,
        "data": {},
    }


def test_after_delete_get_employee_returns_404(client: TestClient) -> None:
    employee_id = _create_employee_id(client)

    delete_response = client.delete(f"/employees/{employee_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/employees/{employee_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {
        "success": False,
        "message": "Employee not found",
        "statusCode": 404,
        "data": {},
    }

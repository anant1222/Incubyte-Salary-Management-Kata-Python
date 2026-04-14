from fastapi.testclient import TestClient


def test_health_returns_unified_success_envelope(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Health check successful",
        "statusCode": 200,
        "data": {"status": "ok"},
    }

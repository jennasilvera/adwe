from fastapi.testclient import TestClient

from adwe.api.app import app


def test_health():
    client = TestClient(app)

    response = client.get("/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

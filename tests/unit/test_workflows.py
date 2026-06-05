from fastapi.testclient import TestClient

from adwe.api.app import app


def test_openapi_exists():
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200

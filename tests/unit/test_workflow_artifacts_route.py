from fastapi.testclient import TestClient

from adwe.api.app import app


def test_workflow_artifacts_route_exists():
    client = TestClient(app)

    response = client.get("/openapi.json")
    paths = response.json()["paths"]

    assert "/v1/workflows/{workflow_id}/artifacts" in paths
